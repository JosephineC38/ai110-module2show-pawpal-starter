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

Yes, one change I made was adding the Owner attribute to the Scheduler class as I forgot
the possibility that a pet can have more than one owner and that the owners could do the tasks at different days. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

It considered time, priority, and preference on some level and I decided that time was the
most important because it helped organize the whole schedule day by day. While priority was
also needed, I thought that it could be adjusted while timing could control how the whole day went. 

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

I used AI tools to debug, create test cases, and to guide me through code that I didn't understand. It also helped me brainstrom when I was stuck during planning. The prompts 
were most helpful when I highlighted certain sections of code that I didn't understand. It
guided me through it line by line and why it worked. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I didn't accept when the AI didn't display priority and duration in the schedule because I felt like those were needed to understand the schedule properly from a first glance. I thought that the context was needed. I evaluated by thinking what I would need from a scheduler. I used my experience from using Google Calendar and thought about what a user
would need from a schedule and how to make it not too confusing. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested happy cases like when there was enough time slots for every tasks, so the schedule
had no conflicts. I also tested for edge cases like if there weren't enough time slots or when there was a werid conflict. They were important because you first needed to know if the app worked properly and test for everything else. Every person has different needs or might 
break the app because they don't know exactly what to do. So you have to test for everything since everything might happen.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am somewhat confident my scheduler works correctly and one edge case I would test is
adding a large amount of pets to see if it would still work. I would also add a varying amount of tasks between them to see if there are any conflicts. I would try to make them add up to more than 24 hours in a day.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfised with the schedule generater and how it could both sort by time and check if there was a conflict in timing.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the app.py by making it more colorful and adding a way to see past schedules or import those schedules. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

That you need to a strong base when designing systems, which can be done through creating a uml diagram with classes and methods.
To test that base, you need to create many test cases and think abou the relationship between classes. 
