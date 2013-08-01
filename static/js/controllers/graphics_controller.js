inepMicrodataApp.controller("graphicsCtrl", ["$scope", "$routeParams", "ScoreSheet", function($scope, $routeParams, ScoreSheet) {
  $scope.schoolCode = $routeParams.schoolCode || "";
  $scope.updateChosenCity($scope.schoolCode);
  getScores();

  function getScores() {
    $scope.error = "";
    $scope.resetInstitutions();

    $scope.showLoader = true;
    ScoreSheet.get({schoolCode: $scope.schoolCode}, function(data) {
      $scope.showLoader = false;
      if (data.error) { $scope.error = data.error; return }

      $scope.schoolName = data.name;
      populateInstitutionData($scope.school, data.school_scores);
      populateInstitutionData($scope.city, data.city_scores);
      populateInstitutionData($scope.state, data.state_scores);

      printGraphics();
    });
  };

  function generateGraphic(field) {
    $("#" + field + ".graphic").highcharts({
      chart: {
        type: 'column'
      },
      title: {
        text: $scope.fieldsNames[field]
      },
      xAxis: {
        title: {
          text: "notas"
        },
        categories: [
          "0-99", "100-199", "200-299",
          "300-399", "400-499", "500-599",
          "600-699", "700-799", "700-799",
          "800-899", "900-1000"
        ]
      },
      yAxis: {
        min: 0,
        max: 100,
        title: {
          text: "percentual"
        }
      },
      series: [
        {
          name: $scope.schoolName,
          data: $scope.school.relative[field]
        },
        {
          name: "Cidade",
          data: $scope.city.relative[field]
        },
        {
          name: "Estado",
          data: $scope.state.relative[field]
        }
      ]
    });
  }

  function printGraphics() {
    for (var field in $scope.school.absolute) {
      generateGraphic(field);
    }
  };

  function populateInstitutionData(institution, data) {
    for (field in data) {
      institution[field] = data[field];
    }
  };

}]);