Call with python3 as follows:

python3 annotation_tool.py 9.jsonl

This will open a GUI so you can annotate all examples in 9.jsonl (it doesn't filter out abstractive/mixed "summaries").
If you close the annotation tool, the annotation will be written INTO THE SAME FILE! Normally, this shouldn't destroy anything.

If you open the annotation tool again, it will start at the first unannotated example in the file.


You might have to adjust some settings to make it look nice on your machine (e.g. because of screen resolution).
You might also want to "pip install ttkthemes" if you want it too look acceptable.
