log

YY Feb 16
1. (fixed) error message: tkinter doesn't have messagebox
(fixed: add "from tkinter import messagebox")
2. (fixed) add context
3. (fixed) simplified the buttons
4. (still ugly) layout: fixed position and window
5. (commented out) selecting datafile is done by python input right now; need to think of a better way. Also input datafile is not going to be in the same directory as the script; need to fix this as well

YY Feb 17
1. (fixed) the progress bar is wrong (fixed)
2. (still ugly) the layout is still awful, buttons are too big! same category maybe have the same bg color?? (partially fixed, layout still not great)
3. (fixed)the output format (fixed)
4. (fixed0 the go-to function is gone now (fixed)
5. (fixed)"previous" is gone (no need)
6. (fixed) if coded, then shown as button_click (partially done)
6. (fixed) see if there is a way to read from the annotated file (fixed)
7. (no need) make the "next" bigger, and away from the coding (no need)
8. (fixed) make sure the coding text is the same as JA's coding (fixed)


YY Feb 19
1. (fixed) subcategories of questions/interrogatives (added)
2. (fixed) the first item "next" not working (ok cheesy solution)
3. (can't be done) make a list of all the annotating categories (not working)
4. (commented out) which directory to work on? (not important)
5. (fixed) the go-to function is gone now (fixed)

Feb 23
1. (fixed) when using "prev", need to stop at -1 (fixed)
2. (fixed) when using "go to", the data between the current and the "go to" is coded as nan. need to make sure that's not going to be an issue (fixed)
3. (fixed) subcategories of questions are still not totally working. need to make sure it is grayed out (fixed)

Feb 24
1. add other syn/sem categories 
2. (fixed) add a button to check if current utt is on the same topic as last utt (fixed)
3. when reading in annot files, check if there exists new columns not coded by JA (fixed)
4. the subcategories of questions need double triple check!!!!!
5. VERY IMPORTANT: If you want to add a category, need to add it in the following places:
**ShowExisting, initialize (initialize attributes), dfResults, at the bottom when initializing results_df**
6. I moved ShowExisting to the end of initialize, but might still be a problem

Feb 25
1. add other syn/sem categories 
2. I moved ShowExisting to the end of initialize, but might still be a problem
3. the subcategories of questions need double triple check!!!!!
4. VERY IMPORTANT: If you want to add a category, need to add it in the following places:
**ShowExisting, initialize (initialize attributes), dfResults, at the bottom when initializing results_df**
5. (you can click on the choice...still not great) subquestions are disabled when Claustype is not interrogative 
6. is there a way to mark where you stopped last time? A button?
7. Layout is still ugly.
