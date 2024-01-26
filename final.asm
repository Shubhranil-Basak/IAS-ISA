LOAD M(35) ; SUB M(29)                                // initializing N-2 
SUB M(29) ; STOR M(36)
LOAD M(28); SUB M(29)                                 // swap = -1
STOR M(31) ; LOAD M(32)                               // i = starting loc of array
STOR M(33) ; LOAD M(33)                               // i = 0+startOfArray
ADD M(29) ; STOR M(34)                                // storing i+1
LOAD M(34) ; STOR M(11,8:19)                          // address modifying for i+1
STOR M(13,8:19) ; STOR M(14,28:39)                    // incase two STORS are required
LOAD M(33) ; STOR M(11,28:39)                         // address modifying for i
STOR M(14,8:19) ; STOR M(15,28:39)                    // incase two STORS are required
LOAD M(132) ; SUB M(131)                              // first x is i+1 second is i
JUMP+ M(17,20:39) ; NOP                               // skip
LOAD M(132) ; STOR M(30)                              // swap starts here
LOAD M(131) ; STOR M(132)                             // swap goes on here
LOAD M(30) ; STOR M(131)                              // swap ends
LOAD M(31) ; ADD M(29)
STOR M(31) ; LOAD M(33)                               // incrementing swap
ADD M(29)  ; STOR M(33)                               // incrementing i
LOAD M(36) ; SUB M(33)                                // checking if it is less than N-2
JUMP+ M(5,20:39) ; LOAD M(31)                         // going back to start but after swap's while loop
JUMP+ M(3,0:19) ; HALT                                // going back to the start just before swap




// memory locations

0                                                     // constant always has 0
1                                                     // constant always has 1
2                                                     // temporary t1
-1                                                    // value of swap
37                                                    // mem address from where the array starts
0                                                     // value of i
0                                                     // value of i+1
43                                                    // value of N (ending location + 1)
42                                                    // value of N-2
10                                                    // values of array
9
10
9
10
11