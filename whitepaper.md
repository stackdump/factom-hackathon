# Solving State Explosion with Petri-Nets and Vector Clocks

#### The Problem

Event driven programming has a problem formally modeling events:
https://en.wikipedia.org/wiki/Event-driven_programming#Criticism

```
Due to the phenomenon known as "state explosion," the complexity of a traditional FSM tends to grow much faster
than the complexity of the reactive system it describes. This happens because the traditional state machine formalism
inflicts repetitions.

```

### Bitwrap's Solution

Q: What is a bitwrap machine? 

A: state machine that can be used to compose a domain specific language for modeling a problem.

This stateful model (when combined with an eventstore database) provides an approachable solution for formal event driven design.

#### Some Computer Science:

Bitwrap converts [Petri-Net Markup Language (PNML)](https://en.wikipedia.org/wiki/Petri_net) definition
to an equivilant state machine.

This state machine form is known as a [Vector Addition System (with States) VASS](https://en.wikipedia.org/wiki/Vector_addition_system)

### VASS state machine example

Given this simple 3-place Petri-Net that models a voting system:

![vote_machine graph](https://bitwrap.github.io/image/vote_machine.png)

* We can represent the state as an array of 'places'.
  * Each place is acted upon by a 'transition' vector.
* We represent an instruction set as a set of deltas
  * Each transition vector maps to a single instruction.
* During an execution
  * Transition vectors are combined with input states using vector addition.
  * Output vectors having only positive scalar integers are valid.

#### State-Vectors

A 3-place Petri-Net - inital state

```
[1,0,0]
```

we execute the 'YAY' instruction
```
 [ 1,0,0]
+[-1,1,0]
 --------
 [ 0,1,0]
```

once this transition happens this graph cannot execute 'YAY' again.


NOTE: Due to the properties of Petri-Nets ( representation with 'tokens')
the valid range of scalar values is constrained to natural numbers. (integers >=0)

```
 [ 0,1,0]
+[-1,1,0]
 --------
 [-1,2,0] <= invalid state
```

Using this machine as a programming model -
we can easily validate the output of our instruction by testing for any negative scalar values.

#### Tic-Tac-Toe w/o State Explosion

Here we show a model for a game of  Tic-Tac-Toe - which is usually difficult to create or conceptualize using 
other types of [Deterministic state machines](https://en.wikipedia.org/wiki/Deterministic_finite_automaton).

Rather than modeling every permutation of the board (as in a DFA)- the Petri-Net model describes the state of the board, and the valid
actions that can be taken from a given input state.

![tic-tac-toe state machine](https://bitwrap.github.io/image/octothorpe.png)

#### Conclusion & Demonstration of Technique

As a programmer this type of state machine is useful in a variety of contexts.

You could use a state machine to represent a traditional workflow or task management system.

Or 

As part of the Domain Driven Design technique - PNML can be used to declare an executable specification for events declared
during an [Event Storming](https://en.wikipedia.org/wiki/Event_Storming) design session.

What is important is that the Petri-Nets help the author keep a clear mental picture of 'what' is being modeled.


#### Learn more

Read our blog: http://www.blahchain.com

To understand more this approach I recommend reading a book by Eric Evans:
[Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.amazon.com/gp/product/0321125215)

