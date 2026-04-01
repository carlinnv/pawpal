# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. 
    -    My initial UML design includes my main classes, including their attributes and methods. I have identified four main classes: User, Pet, Task, and Schedule. Users will be able to specify their own preferences, which will help with identifying constraints later when developing schedules. They will also be able to specify their pets' traits. Users should also be able to schedule tasks, and lastly, create a daily schedule along with explanations. 
- What classes did you include, and what responsibilities did you assign to each?
    - I included the User, Pet, Task, and Schedule classes. The User class should store all of the users' characteristics, such as their preferences and availabilities. The Pet should include the pets' needs, such as their hunger and energy. The Tasks would include things like walking and feeding, and would be used by the User to keep track of and fulfill their Pets' needs. Lastly, the User would be able to generate a daily Schedule that includes all of the tasks for a specific pet. 

**b. Design changes**

- Did your design change during implementation?
    - Yes, they did. I asked Copilot to describe any missing relationships, as well as to name certain attributes that would most likely not be used at runtime. Based on Chat's suggestions, I added/changed certain relationships for the classes so that the attributes would actually be used in the program. 
- If yes, describe at least one change and why you made it.
    - One of the changes concerned the "Date" attribute in the Schedule class I created. Originally, the date was not used at all in the relationship between classes, making it a redundant attribute. After consulting Copilot, I decided to make it so that each Schedule had to be linked back to a User. This way, the User can refer back to previous schedules using the Date attribute. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
