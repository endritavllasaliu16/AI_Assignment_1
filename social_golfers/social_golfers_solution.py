"""
Social Golfers Problem - EXHAUSTIVE Uninformed Search
Trying to reach Week 7+ with PURE uninformed search
Deep backtracking - trying different group formation orders
"""

import time
from typing import List, Optional, Set
import copy
import itertools

class ExhaustiveUninformedSearch:
    def __init__(self, num_golfers=32, group_size=4):
        self.num_golfers = num_golfers
        self.group_size = group_size
        self.num_groups = num_golfers // group_size
        self.played_together = set()
        self.best_schedule = []
        self.attempts = 0
        
    def reset(self):
        self.played_together = set()
    
    def is_valid_group(self, group: List[int]) -> bool:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                pair = tuple(sorted([group[i], group[j]]))
                if pair in self.played_together:
                    return False
        return True
    
    def add_group_pairs(self, group: List[int]):
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                self.played_together.add(tuple(sorted([group[i], group[j]])))
    
    def remove_group_pairs(self, group: List[int]):
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                self.played_together.discard(tuple(sorted([group[i], group[j]])))
    
    def exhaustive_dfs(self, target_weeks: int, timeout: int = 300) -> List[List[List[int]]]:
        """
        EXHAUSTIVE DFS - tries MULTIPLE different orderings
        This explores different paths through the search space
        Still uninformed - just more thorough
        """
        self.reset()
        best_schedule = []
        start_time = time.time()
        
        print(f"🔍 EXHAUSTIVE UNINFORMED SEARCH")
        print(f"🎯 Target: {target_weeks} weeks")
        print(f"⏱️  Timeout: {timeout}s")
        print(f"📊 Strategy: Try multiple group formation orderings")
        print(f"⚠️  Still NO heuristics - just more exhaustive\n")
        
        # Try different starting orderings for group formation
        # This is still uninformed - we're not being smart, just more thorough
        orderings_tried = 0
        
        try:
            # Try different permutations of how we form the first week
            # This explores different branches of the search tree
            for first_week_attempt in range(100):  # Try 100 different ways
                if time.time() - start_time > timeout:
                    break
                
                orderings_tried += 1
                self.reset()
                schedule = []
                
                # Build schedule with this particular ordering
                success = self._build_schedule_exhaustive(
                    schedule, target_weeks, first_week_attempt
                )
                
                if len(schedule) > len(best_schedule):
                    best_schedule = copy.deepcopy(schedule)
                    elapsed = time.time() - start_time
                    print(f"✨ Attempt {orderings_tried}: {len(schedule)} WEEKS! (t={elapsed:.1f}s)")
                    
                    if len(schedule) >= target_weeks:
                        print(f"\n🎉 SUCCESS! Reached {target_weeks} weeks!")
                        return best_schedule
                
                if orderings_tried % 10 == 0:
                    print(f"   Tried {orderings_tried} orderings, best: {len(best_schedule)} weeks")
        
        except KeyboardInterrupt:
            print(f"\n⏹️  Stopped by user")
        
        elapsed = time.time() - start_time
        print(f"\n📊 Exhausted {orderings_tried} different orderings")
        print(f"⏱️  Time: {elapsed:.1f}s")
        print(f"🏆 Best: {len(best_schedule)} weeks")
        
        return best_schedule
    
    def _build_schedule_exhaustive(self, schedule: List[List[List[int]]], 
                                   target_weeks: int, seed: int) -> bool:
        """Build schedule trying different group formations"""
        for week_num in range(target_weeks):
            # Try to build this week with backtracking on group formation order
            week = []
            available = list(range(self.num_golfers))
            
            # Use seed to vary the exploration order (still systematic, not random)
            offset = (seed * 7 + week_num * 3) % self.num_golfers
            
            if self._build_week_with_backtrack(week, available, offset):
                schedule.append(week)
                for group in week:
                    self.add_group_pairs(group)
            else:
                return False
        
        return True
    
    def _build_week_with_backtrack(self, week: List[List[int]], 
                                   available: List[int], offset: int) -> bool:
        """Build one week with deep backtracking on group choices"""
        if len(week) == self.num_groups:
            return len(available) == 0
        
        if len(available) < self.group_size:
            return False
        
        # Try different starting golfers (offset varies which we try first)
        for start_idx in range(min(len(available), 8)):  # Try up to 8 different starting points
            idx = (start_idx + offset) % len(available)
            first_golfer = available[idx]
            
            # Try to build a group starting with this golfer
            group = [first_golfer]
            remaining = [g for g in available if g != first_golfer]
            
            if self._complete_group_exhaustive(group, remaining, 0):
                week.append(group[:])
                new_available = [g for g in available if g not in group]
                
                # Try to build rest of week
                if self._build_week_with_backtrack(week, new_available, offset):
                    return True
                
                # Backtrack
                week.pop()
        
        return False
    
    def _complete_group_exhaustive(self, group: List[int], 
                                   available: List[int], start: int) -> bool:
        """Complete a group by trying all valid combinations"""
        if len(group) == self.group_size:
            return self.is_valid_group(group)
        
        # Try each golfer
        for i in range(start, len(available)):
            golfer = available[i]
            group.append(golfer)
            
            if self._complete_group_exhaustive(group, available, i + 1):
                return True
            
            group.pop()
        
        return False
    
    def depth_limited_exhaustive(self, target_weeks: int, timeout: int = 300) -> List[List[List[int]]]:
        """
        DLS with more exhaustive exploration
        Tries backtracking at the week level too
        """
        self.reset()
        best_schedule = []
        start_time = time.time()
        
        print(f"\n{'='*70}")
        print(f"🔍 DEPTH LIMITED SEARCH - EXHAUSTIVE")
        print(f"🎯 Target: {target_weeks} weeks")
        print(f"⏱️  Timeout: {timeout}s\n")
        
        try:
            # Try different paths through the search tree
            for attempt in range(50):
                if time.time() - start_time > timeout:
                    break
                
                self.reset()
                schedule = []
                
                # Build with backtracking
                self._dls_recursive(schedule, 0, target_weeks, attempt)
                
                if len(schedule) > len(best_schedule):
                    best_schedule = copy.deepcopy(schedule)
                    elapsed = time.time() - start_time
                    print(f"✨ Attempt {attempt + 1}: {len(schedule)} weeks (t={elapsed:.1f}s)")
                    
                    if len(schedule) >= target_weeks:
                        print(f"\n🎉 SUCCESS! Reached {target_weeks} weeks!")
                        return best_schedule
        
        except KeyboardInterrupt:
            print(f"\n⏹️  Stopped")
        
        return best_schedule
    
    def _dls_recursive(self, schedule: List[List[List[int]]], 
                      depth: int, max_depth: int, seed: int) -> bool:
        if depth >= max_depth:
            return True
        
        # Try to build next week
        week = []
        available = list(range(self.num_golfers))
        offset = (seed * 11 + depth * 5) % self.num_golfers
        
        if self._build_week_with_backtrack(week, available, offset):
            schedule.append(week)
            for group in week:
                self.add_group_pairs(group)
            
            # Recurse
            result = self._dls_recursive(schedule, depth + 1, max_depth, seed)
            
            if not result:
                # Backtrack
                for group in week:
                    self.remove_group_pairs(group)
                schedule.pop()
            
            return result
        
        return False
    
    def print_schedule(self, schedule: List[List[List[int]]], title: str):
        if not schedule:
            print(f"\n❌ No schedule found\n")
            return
        
        print(f"\n{'='*70}")
        print(f"{title}")
        print(f"{'='*70}")
        print(f"🎉 Achieved: {len(schedule)} WEEKS\n")
        
        for week_num, week in enumerate(schedule, 1):
            print(f"Week {week_num}:")
            for group_num, group in enumerate(week, 1):
                print(f"  Group {group_num}: {sorted(group)}")
            print()
        
        # Verify
        pairs = set()
        conflicts = 0
        for week in schedule:
            for group in week:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        pair = tuple(sorted([group[i], group[j]]))
                        if pair in pairs:
                            conflicts += 1
                        pairs.add(pair)
        
        print(f"{'='*70}")
        if conflicts == 0:
            print(f"✅ VERIFIED: No conflicts!")
        else:
            print(f"❌ {conflicts} conflicts found")
        
        print(f"📊 Unique pairs: {len(pairs)}/496 ({100*len(pairs)/496:.1f}%)")
        print(f"{'='*70}\n")


def main():
    print("="*70)
    print("SOCIAL GOLFERS - WEEK 7 CHALLENGE")
    print("Exhaustive Uninformed Search")
    print("="*70)
    print()
    
    solver = ExhaustiveUninformedSearch()
    
    # Try with exhaustive DFS
    schedule = solver.exhaustive_dfs(target_weeks=7, timeout=300)
    solver.print_schedule(schedule, "EXHAUSTIVE DFS RESULTS")
    
    # If that didn't work, try DLS
    if len(schedule) < 7:
        print("\n🔄 Trying Depth Limited Search...")
        schedule2 = solver.depth_limited_exhaustive(target_weeks=7, timeout=300)
        
        if len(schedule2) > len(schedule):
            schedule = schedule2
            solver.print_schedule(schedule, "DEPTH LIMITED SEARCH RESULTS")


if __name__ == "__main__":
    main()