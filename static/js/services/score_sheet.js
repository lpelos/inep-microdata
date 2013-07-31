inepMicrodataApp.factory("ScoreSheet", ["$resource", function($resource) {
  return $resource("/histograms/:year/schools/:schoolCode", { year: 2011, schoolCode: "" });
}]);