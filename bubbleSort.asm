LOAD M(regN) ; SUB M(reg1)                            // initializing N-2 
SUB M(reg1) ; STOR M(regN)
LOAD M(s0); SUB M(-1)                                 // swap = -1
STOR M(swap) ; LOAD (s0)
STOR M(regi) ; NOP                                    // i = 0
ADD M(1) ; STOR (regi+1)                              // storing i+1
LOAD M(regi+1) ; STOR M(nextLine,8:19)                // address modifying for i+1
NOP ; NOP                                             // incase two STORS are required
LOAD M(regi) ; STOR M(nextLine,8:19)                  // address modifying for i
NOP ; NOP                                             // incase two STORS are required
LOAD M(a[i+1]) ; SUB M(a[i])                          // first x is i+1 second is i
JUMP+ (ENDofInnerWhileLoop,0:19) ; NOP                // skip
LOAD M(a[i+1]) ; STOR M(t1)                           // swap starts here
LOAD M(a[i]) ; STOR M(a[i+1])                         // swap goes on here
LOAD M(t1) ; STOR M(a[i])                             // swap ends
LOAD (swap) ; ADD M(reg1)                             // incrementing swap
LOAD (regi) ; ADD M(reg1)                             // incrementing i
LOAD M(reg(n-2)) ; SUB (i)                            // checking if it is less than N-2
JUMP+ (justAfterSwap,0:19) ; LOAD (swap)              // going back to start but after swap's while loop
JUMP+ (justBeforeSwao,0:19) ; HALT                    // going back to the start just before swap

// memory locations

1                                                     // constant always has 1
2                                                     // temporary t1
