#!/bin/bash
python stolen_probability.py
python stolen_probability_with_convex.py
python plot_bounded.py  --ids-file datafiles/bounded.txt --title "bounded models"
python plot_row_iterations.py --ids-file datafiles/zhen_l2r_exp_ids.txt  --title 'Identical models from an ensemble differ'
python plot_row_iterations.py --ids-file datafiles/teacher_exp_ids.txt  --title 'Teacher models'
python plot_row_iterations.py --ids-file datafiles/student_exp_ids.txt  --title 'Student models'
python plot_row_iterations.py --ids-file datafiles/lms.txt  --title 'Language Models'
python plot_random_iterations.py --ids-file datafiles/uniform_exp_ids.txt
