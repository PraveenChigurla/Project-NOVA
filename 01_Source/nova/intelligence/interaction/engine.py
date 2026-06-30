"""
Interaction Engine.
Calculates realistic human interaction streams (Bezier curves, timings).
"""
import math
import random
from typing import List, Tuple
import logging

from nova.intelligence.interaction.models import MovementProfile, InteractionConfig

logger = logging.getLogger(__name__)

class InteractionEngine:
    """Generates mathematically human-like interaction streams."""
    
    def __init__(self, config: InteractionConfig = None):
        self.config = config or InteractionConfig()
        
    def generate_movement_stream(self, start_x: int, start_y: int, end_x: int, end_y: int, profile: MovementProfile = None) -> List[Tuple[int, int, float]]:
        """
        Generates a sequence of (x, y, delay_after_ms) tuples.
        """
        prof = profile or self.config.profile
        logger.debug(f"Generating {prof.value} movement stream from ({start_x},{start_y}) to ({end_x},{end_y})")
        
        if prof == MovementProfile.INSTANT:
            return [(end_x, end_y, 0.0)]
            
        # Calculate distance
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        
        # Determine number of steps (resolution of the curve)
        if prof == MovementProfile.FAST:
            steps = min(int(distance / 20), 10)
        else:
            steps = min(int(distance / 10), 50)
            
        steps = max(steps, 2)
        
        # Generate points
        if prof == MovementProfile.FAST:
            # Linear interpolation
            points = self._generate_linear(start_x, start_y, end_x, end_y, steps)
        else:
            # Bezier interpolation with jitter
            points = self._generate_bezier(start_x, start_y, end_x, end_y, steps, self.config.jitter)
            
        # Generate timings (Acceleration/Deceleration)
        timings = self._generate_timings(steps, prof)
        
        stream = []
        for i in range(steps):
            x, y = points[i]
            stream.append((int(x), int(y), timings[i]))
            
        # Ensure exact final coordinate
        stream.append((end_x, end_y, 0.0))
        
        return stream

    def _generate_linear(self, x1, y1, x2, y2, steps) -> List[Tuple[float, float]]:
        points = []
        for i in range(steps):
            t = i / float(steps - 1)
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            points.append((x, y))
        return points

    def _generate_bezier(self, x1, y1, x2, y2, steps, jitter) -> List[Tuple[float, float]]:
        """Generates a cubic bezier curve with randomized control points to simulate human imperfection."""
        # Calculate intermediate control points
        # Add random offset proportional to distance and jitter
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        offset = dist * jitter
        
        # Control point 1 (1/3rd of the way there, plus random offset)
        cx1 = x1 + (x2 - x1) * 0.33 + random.uniform(-offset, offset)
        cy1 = y1 + (y2 - y1) * 0.33 + random.uniform(-offset, offset)
        
        # Control point 2 (2/3rds of the way there, plus random offset)
        cx2 = x1 + (x2 - x1) * 0.66 + random.uniform(-offset, offset)
        cy2 = y1 + (y2 - y1) * 0.66 + random.uniform(-offset, offset)
        
        points = []
        for i in range(steps):
            t = i / float(steps - 1)
            # Cubic bezier formula
            u = 1 - t
            tt = t * t
            uu = u * u
            uuu = uu * u
            ttt = tt * t
            
            p_x = uuu * x1 + 3 * uu * t * cx1 + 3 * u * tt * cx2 + ttt * x2
            p_y = uuu * y1 + 3 * uu * t * cy1 + 3 * u * tt * cy2 + ttt * y2
            
            points.append((p_x, p_y))
            
        return points

    def _generate_timings(self, steps: int, profile: MovementProfile) -> List[float]:
        """
        Generates millisecond delays for each step to simulate ease-in/ease-out.
        Returns delays in seconds.
        """
        timings = []
        
        # Base duration in seconds depending on profile
        if profile == MovementProfile.FAST:
            base_duration = 0.1
        elif profile == MovementProfile.NATURAL:
            base_duration = random.uniform(0.3, 0.6)
        else: # PRECISE
            base_duration = random.uniform(0.6, 1.2)
            
        # Distribute time across steps using a sine wave for ease-in-out
        total_weight = 0
        weights = []
        for i in range(steps):
            # sin(0 to pi) creates a curve that is 0 at ends and 1 in middle
            # We invert it because we want *longer* delays at the ends (slower movement)
            # and *shorter* delays in the middle (faster movement)
            t = i / float(steps - 1) if steps > 1 else 0
            speed_curve = math.sin(t * math.pi) 
            delay_weight = 1.0 - (speed_curve * 0.8) # Keep some base delay (0.2) in middle
            weights.append(delay_weight)
            total_weight += delay_weight
            
        # Normalize weights to base_duration
        for w in weights:
            step_duration = (w / total_weight) * base_duration
            timings.append(step_duration)
            
        return timings
