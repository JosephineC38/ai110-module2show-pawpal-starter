# PawPal+ Project Reflection

## 1. System Design

Three Core Actions
- Add/Remove Pets along with their basic information 
- Schedule a walk based on time schedules and when the pet feels happy  
- See today's tasks for the pet and what needs to be done 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design contains the classes: Owner, Pet, Task, and Scheduler. The Owner is for the pet owner and it owns the Pet and has the attributes of name, preferences, available_time, and pets. It is meant to see as an overview for the user and for them to add their availabilty. The Owner class can add/remove pets, and change its other attributes through methods. The Pet class is for each pet that the owner has and it can have many objects from the Task class. It's mean to see what each pet needs at any time and to build a profile of them. It has the attributes name, animal_type, health, age, breed, special_needs, and tasks. It can use different methods to update these attributes. The Task class are for the pets and can be organized through the Scheduler class. It is meant to easily see what needs to be done for the Pets. It has the attributes of type, time, importance, occurance,  description, duration_minutes, completed, and recurring with methods to update each one. The final class is the Scheduler class, which neatly organizes tasks for the user to view. It has the attributes of time, importance, blockers, daily_time_limit, and available_slots. Based on these attributes, the class can generate plans, prioritize tasks, resolve blockers, and explain why the plan was created. 


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---
Yes, one change I made was adding the Owner attribute to the Scheduler class as I forgot
the possibility that a pet can have more than one owner and that the owners could do the tasks at different days. 

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Because of the built-in methods for resolving blockers, detecting conflicts, and checking when two tasks share the same slot, the tradeoff here is you can't overlap tasks. However, 
it's reasonable because the tasks are unlikely to be doable at the same time. For example,
you can't feed and walk your pet at once. Futhermore, it's only a scheduler for pets, not for other tasks, so nothing needs to overlap and is useful if someone else needs to take care of your pet. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
