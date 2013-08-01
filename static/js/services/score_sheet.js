inepMicrodataApp.factory("ScoreSheet", ["$resource", function($resource) {
  return $resource("/api/histograms/:year/schools/:schoolCode", { year: 2011, schoolCode: "" });
}]);