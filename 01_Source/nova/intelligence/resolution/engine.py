"""
Target Resolution Engine.
Resolves Semantic Targets within a VisionResult (World Model).
"""
import logging
import math
from typing import List, Optional, Tuple, Union

from nova.intelligence.vision.models import VisionResult, DetectedRegion, DetectedText, DetectedObject, BoundingBox
from nova.intelligence.resolution.models import TargetQuery, ResolvedTarget, SpatialRelation

logger = logging.getLogger(__name__)

class TargetResolutionEngine:
    """The Spatial and Semantic Reasoning Brain of NOVA."""
    
    def resolve(self, world_model: VisionResult, query: TargetQuery) -> Optional[ResolvedTarget]:
        """
        Executes a geometric and semantic query against the World Model.
        """
        logger.info(f"Resolving query: Target='{query.target_text}' Relation={query.relation} Reference='{query.reference_text}'")
        
        # 1. Find all candidate targets matching the primary text
        candidates = self._find_candidates(world_model, query.target_text, query.target_type)
        if not candidates:
            logger.warning(f"Failed to resolve: No semantic candidates found for '{query.target_text}'")
            return None
            
        logger.debug(f"Found {len(candidates)} candidate(s) for '{query.target_text}'")
        
        # If there's no spatial relation required, just return the best candidate
        if not query.relation or not query.reference_text:
            best_candidate = self._rank_candidates_simple(candidates)
            return self._build_resolved_target(best_candidate, "Primary text match (No spatial relation provided).")
            
        # 2. Find the reference anchor
        anchors = self._find_candidates(world_model, query.reference_text, query.reference_type)
        if not anchors:
            logger.warning(f"Failed to resolve: No reference anchors found for '{query.reference_text}'")
            return None
            
        # For simplicity, we assume the best anchor is the first one if multiple exist.
        # In a highly advanced version, we would evaluate all candidate-anchor pairs.
        anchor = self._rank_candidates_simple(anchors)
        logger.debug(f"Using anchor '{query.reference_text}' at {anchor.box}")
        
        # 3. Filter candidates by Spatial Relation
        valid_candidates = self._filter_by_spatial_relation(candidates, anchor, query.relation)
        
        if not valid_candidates:
            logger.warning(f"Failed to resolve: {len(candidates)} targets found, but none satisfied {query.relation} relative to '{query.reference_text}'")
            return None
            
        # 4. Rank remaining candidates by proximity to anchor
        best_candidate = self._rank_by_proximity(valid_candidates, anchor)
        
        reason = f"Ranked #1 out of {len(valid_candidates)} candidates matching spatial relation {query.relation.value.upper()} anchor '{query.reference_text}'."
        return self._build_resolved_target(best_candidate, reason)

    # =========================================================================
    # SEMANTIC MATCHING
    # =========================================================================

    def _find_candidates(self, world_model: VisionResult, text: str, type_filter: Optional[str] = None) -> List[Union[DetectedText, DetectedObject]]:
        """Finds all regions in the world model that fuzzily/exactly match the text."""
        candidates = []
        target = text.lower().strip()
        
        # Search Text
        if not type_filter or type_filter == "text":
            for t in world_model.text:
                if target in t.text.lower():
                    candidates.append(t)
                    
        # Search Objects
        if not type_filter or type_filter != "text":
            for o in world_model.objects:
                # Match label or semantic text
                if (o.text and target in o.text.lower()) or (target in o.label.lower()):
                    if not type_filter or o.label.lower() == type_filter.lower():
                        candidates.append(o)
                        
        return candidates

    def _rank_candidates_simple(self, candidates: List[Union[DetectedText, DetectedObject]]) -> Union[DetectedText, DetectedObject]:
        """Ranks purely by vision provider confidence."""
        return sorted(candidates, key=lambda c: c.confidence, reverse=True)[0]

    def _build_resolved_target(self, candidate: Union[DetectedText, DetectedObject], reason: str) -> ResolvedTarget:
        semantic_label = candidate.text if isinstance(candidate, DetectedText) else (candidate.text or candidate.label)
        return ResolvedTarget(
            box=candidate.box,
            semantic_label=semantic_label,
            confidence=candidate.confidence,
            reason=reason
        )

    # =========================================================================
    # SPATIAL REASONING MATH
    # =========================================================================

    def _filter_by_spatial_relation(self, candidates: List[DetectedRegion], anchor: DetectedRegion, relation: SpatialRelation) -> List[DetectedRegion]:
        """Filters candidates using bounding box geometry."""
        valid = []
        ax, ay = anchor.box.center_x, anchor.box.center_y
        
        for c in candidates:
            cx, cy = c.box.center_x, c.box.center_y
            
            if relation == SpatialRelation.ABOVE:
                if cy < ay: valid.append(c)
            elif relation == SpatialRelation.BELOW:
                if cy > ay: valid.append(c)
            elif relation == SpatialRelation.LEFT_OF:
                if cx < ax: valid.append(c)
            elif relation == SpatialRelation.RIGHT_OF:
                if cx > ax: valid.append(c)
            elif relation == SpatialRelation.INSIDE:
                if (c.box.left >= anchor.box.left and 
                    c.box.top >= anchor.box.top and 
                    (c.box.left + c.box.width) <= (anchor.box.left + anchor.box.width) and 
                    (c.box.top + c.box.height) <= (anchor.box.top + anchor.box.height)):
                    valid.append(c)
            elif relation == SpatialRelation.CONTAINS:
                if (anchor.box.left >= c.box.left and 
                    anchor.box.top >= c.box.top and 
                    (anchor.box.left + anchor.box.width) <= (c.box.left + c.box.width) and 
                    (anchor.box.top + anchor.box.height) <= (c.box.top + c.box.height)):
                    valid.append(c)
            elif relation == SpatialRelation.NEAREST:
                valid.append(c) # All are valid for nearest, ranking will sort them
                
        return valid

    def _rank_by_proximity(self, candidates: List[DetectedRegion], anchor: DetectedRegion) -> DetectedRegion:
        """Ranks candidates by Euclidean distance to the anchor."""
        ax, ay = anchor.box.center_x, anchor.box.center_y
        
        def distance(c: DetectedRegion) -> float:
            cx, cy = c.box.center_x, c.box.center_y
            return math.sqrt((cx - ax)**2 + (cy - ay)**2)
            
        return sorted(candidates, key=distance)[0]
