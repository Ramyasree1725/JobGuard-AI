"""
JobGuard Core Workflow - Finite State Machine (FSM) & Transition Guard Engine
Enforces formal lifecycle transitions for job posts, candidate verification audits,
and police complaint draft workflows.
"""

from typing import Dict, List, Optional, Callable, Any, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class GuardResult:
    allowed: bool
    reason: str = ""


@dataclass
class Transition:
    source_state: str
    target_state: str
    trigger_event: str
    guard_fn: Optional[Callable[[Dict[str, Any]], GuardResult]] = None
    action_fn: Optional[Callable[[Dict[str, Any]], None]] = None


@dataclass
class StateNode:
    name: str
    is_initial: bool = False
    is_terminal: bool = False
    entry_action: Optional[Callable[[Dict[str, Any]], None]] = None
    exit_action: Optional[Callable[[Dict[str, Any]], None]] = None


class StateMachine:
    """Deterministic Finite State Machine with transition guards and side-effect hooks."""

    def __init__(self, name: str, initial_state: str):
        self.name = name
        self.initial_state = initial_state
        self.current_state = initial_state
        self._states: Dict[str, StateNode] = {}
        self._transitions: List[Transition] = []
        self._context: Dict[str, Any] = {}
        self._history: List[Tuple[str, str, str]] = []  # (source, event, target)

    def add_state(self, state: StateNode) -> "StateMachine":
        self._states[state.name] = state
        return self

    def add_transition(self, transition: Transition) -> "StateMachine":
        self._transitions.append(transition)
        return self

    def trigger(self, event: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Trigger an event transition from the current state."""
        ctx = dict(self._context)
        if payload:
            ctx.update(payload)

        # Find matching transition
        matching = [
            t for t in self._transitions
            if t.source_state == self.current_state and t.trigger_event == event
        ]

        if not matching:
            return False, f"Invalid transition: No transition defined for event '{event}' from state '{self.current_state}'"

        transition = matching[0]

        # Evaluate guard condition if present
        if transition.guard_fn:
            guard_res = transition.guard_fn(ctx)
            if not guard_res.allowed:
                return False, f"Guard rejected transition: {guard_res.reason}"

        # Execute exit action of source state
        source_node = self._states.get(self.current_state)
        if source_node and source_node.exit_action:
            source_node.exit_action(ctx)

        # Execute transition action
        if transition.action_fn:
            transition.action_fn(ctx)

        # Execute entry action of target state
        target_node = self._states.get(transition.target_state)
        if target_node and target_node.entry_action:
            target_node.entry_action(ctx)

        self._history.append((self.current_state, event, transition.target_state))
        self.current_state = transition.target_state
        self._context = ctx

        return True, f"Successfully transitioned to '{self.current_state}'"

    def get_history(self) -> List[Tuple[str, str, str]]:
        return list(self._history)
