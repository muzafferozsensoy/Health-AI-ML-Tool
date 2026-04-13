import KNNVisualization from './KNNVisualization';
import SVMVisualization from './SVMVisualization';
import DecisionTreeVisualization from './DecisionTreeVisualization';
import RandomForestVisualization from './RandomForestVisualization';
import LogisticRegressionVisualization from './LogisticRegressionVisualization';
import NaiveBayesVisualization from './NaiveBayesVisualization';

const TYPE_MAP = {
  knn: KNNVisualization,
  svm: SVMVisualization,
  decision_tree: DecisionTreeVisualization,
  random_forest: RandomForestVisualization,
  logistic_regression: LogisticRegressionVisualization,
  naive_bayes: NaiveBayesVisualization,
};

// Frontend model IDs → backend visualization types
const FRONTEND_TO_TYPE = {
  knn: 'knn',
  svm: 'svm',
  dt: 'decision_tree',
  rf: 'random_forest',
  lr: 'logistic_regression',
  nb: 'naive_bayes',
};

export default function ModelVisualization({ data, modelId }) {
  if (!data) return null;

  const type = data.type ?? FRONTEND_TO_TYPE[modelId];
  const Component = TYPE_MAP[type];

  if (!Component) return null;
  return <Component data={data} />;
}
