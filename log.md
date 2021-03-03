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
**ShowExisting, initialize (initialize attributes), dfResults, Goto (when resetting everything), datacleanup**
5. (you can click on the choice...still not great) subquestions are disabled when Claustype is not interrogative 
6. is there a way to mark where you stopped last time? A button?
7. Followup only show up when the first prev is pressed; why?
8. why does sometimes when you not press "followup" it's "nan" and some other time it's "0"???? <https://stackoverflow.com/questions/43254699/pandas-to-dict-returns-none-mixed-with-nan> says it's probably a problem with pandas and dict conversion. May have to convert everything to dataframe
-- so I can't use IntVar; the "nan"s are giving me a hard time
9. (done) I changed the column names from *subI* to *SubI*
10. (done) first item won't be coded for followup

Feb 27
1. followup is good again! But still don't know why. May need to go back to the coded files to change things
2. combined "next" and "goto"
3.  **need attention** need to have a mechanism where if the subquestions are disabled, the subq buttons reset and the results for sub questions are recorded as NaN. 
<<<<<<< HEAD
4. (fixed) Frames
5. (fixed) add more categories (ones that AJ coded at least; but also maybe the here&now, desirable) 

Feb 28
1. fixed followup by reading in "FollowUp?" as Int64, and fillna("0")
2. changed layout
3. Followup Button: I've tried this with other things, but if I switch to another app (window) and switch back, followup button is all of a suddon not greyed out. Might be my laptop's problem
4. VERY IMPORTANT: If you want to add a category, need to add it in the following places:
**ShowExisting, initialize, dfResults, Goto (when resetting everything), and previously coded data**
5. added syntactic features 
6. (fixed!!! by getting rid of NaN at the dataframe level) regroup some categories, still don't know why sometimes it's NaN, sometimes it's not

Mar 1
1. added discourse features
2. **needs attention** the updated PHON data is not reading in the result file :/ maybe always have a mechanism to paste updated PHON data in with the resultfile? I'm not sure if there's a good solution.
3. (fixed) need to have a mechanism where if the subquestions are disabled, the subq buttons reset and the results for sub questions are recorded as NaN.
4. add a "pointer" to the data that's coded before exit, and read in the last item coded? maybe more trouble than its worth
5. 
=======
4. **need attention** Frames
5. **need attention** add more categories (ones that AJ coded at least; but also maybe the here&now, desirable) 

>>>>>>> parent of 984f9d8... added synfeatures, reconfig the layout


Mar 3
- screwed up the data intake; had to revert back to Sunday's commit. Turns out I missed a comma...
- can select data with dialogue
- **Need Attention** build a repo for data and dataprocessing
- seperate comment and situation
