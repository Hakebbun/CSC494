# Short script to build a new classifer then immediately test it.
# Uses 1250 features and .90 confidence cutoff by default

python buildClassifier.py 1250
python testClassifier.py .90
