## Reasons as to why I am switching to OOPs now

### Inheritance
1. Database can perform certain functions/operations
2. SysAdmin can also perform all the functions that database does and some specialised functions
3. CampAdmin also can perform all the functions that a database can, alongwith some specialised functions of its own

- That's why SysAdmin and CampAdmin are classes inheriting Database (so `inheritance` is a reason)

### Security
1. The specialised functions of SysAdmin are not available to CampAdmin and vice versa. So classes provide this security as an object of CampAdmin can't access SysAdmin class and vice versa.

- This is security and seperation of specialised operations (so `security` is a reason)

### Abstraction
1. Abstraction is a reason: because the SysAdmin / CampAdmin only needs to do the functions they can do, and how it is done is hidden from everyone

### Polymorphism
1. Function Overriding is a reason: because SysAdmin may also do read operation, and CampAdmin can also do read operation, but the internal working of both will be different and results will also be different for same function performed (basically it is `polymorphism`, so it's a reason)

### Modularity
1. The SysAdmin class and CampAdmin classes can be kept as different modules, making the project simple and the modules reusable. 
- So `modularity` is a reason.

### Encapsulation
1. All the functions/behaviors or data members of SysAdmin/CampAdmin are wrapped in their respective classes. This is encapsulation. Just need to create an instance of a class, and it has all those properties that class specifies. 
- So `encapsulation` is a reason.

+ These are all the reasons I have, and are enough for me to proceed with OOPs style now.
