from sklearn import datasets
from sklearn import linear_model
from sklearn import metrics
from sklearn import model_selection
from sklearn import pipeline
from sklearn import preprocessing

# Load the data
dataset = datasets.load_breast_cancer()
print(dataset.DESCR)

X, y = dataset.data, dataset.target
print(X[0])

# Define the steps of the model
model = pipeline.Pipeline([
    ('scale', preprocessing.StandardScaler()),
    ('logistic_reg', linear_model.LogisticRegression(solver='lbfgs'))
])

# Define a determistic cross-validation procedure
cv = model_selection.KFold(n_splits=7, shuffle=True, random_state=42)

# Compute the MSE values
scorer = metrics.make_scorer(metrics.roc_auc_score)
scores = model_selection.cross_val_score(model, X, y, scoring=scorer, cv=cv)

# Display the average score and it's standard deviation
print(f'ROC AUC: {scores.mean():.3f} (± {scores.std():.3f})')
