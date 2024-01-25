LOAD M(34) ; SUB M(28)                                // initializing N-2 
SUB M(28) ; STOR M(35)
LOAD M(27); SUB M(28)                                 // swap = -1
STOR M(30) ; LOAD M(31)                               // i = starting loc of array
STOR M(32) ; NOP                                      // i = 0
ADD M(28) ; STOR M(33)                                // storing i+1
LOAD M(33) ; STOR M(11,8:19)                          // address modifying for i+1
STOR M(13,8:19) ; STOR M(14,28:39)                    // incase two STORS are required
LOAD M(32) ; STOR M(11,28:39)                         // address modifying for i
STOR M(14,8:19) ; STOR M(15,28:39)                    // incase two STORS are required
LOAD M(132) ; SUB M(131)                              // first x is i+1 second is i
JUMP+ M(17,0:19) ; NOP                                // skip
LOAD M(132) ; STOR M(29)                              // swap starts here
LOAD M(131) ; STOR M(132)                             // swap goes on here
LOAD M(29) ; STOR M(131)                              // swap ends
LOAD M(30) ; ADD M(28)                                // incrementing swap
LOAD M(32) ; ADD M(28)                                // incrementing i
LOAD M(34) ; SUB M(32)                                // checking if it is less than N-2
JUMP+ M(7,0:19) ; LOAD M(30)                          // going back to start but after swap's while loop
JUMP+ M(3,0:19) ; HALT                                // going back to the start just before swap




// memory locations

0                                                     // constant always has 0
1                                                     // constant always has 1
2                                                     // temporary t1
-1                                                    // value of swap
36                                                    // mem address from where the array starts
0                                                     // value of i
0                                                     // value of i+1
41                                                    // value of N
5                                                     // value of N-2
5                                                     // values of array
4
3
2
1