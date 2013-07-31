inepMicrodataApp.controller("histogramsCtrl", ["$scope", "ScoreSheet", function($scope, ScoreSheet) {
  $scope.fieldsNames = {
    ch: "Ciências Humanas",
    cn: "Ciências da Natureza",
    lc: "Líguas e Códigos",
    mt: "Matemática"
  }
  $scope.chosenCity = "";
  resetInstitutions();

  $scope.getScores = function() {
    $scope.error = "";
    resetInstitutions();

    ScoreSheet.get({schoolCode: $scope.chosenCity}, function(data) {
      if (data.error) { $scope.error = data.error; return }

      $scope.schoolName = data.name;
      populateInstitutionData($scope.school, data.school_scores);
      populateInstitutionData($scope.city, data.city_scores);
      populateInstitutionData($scope.state, data.state_scores);

      generateGraphics();
    });
  };

  function generateGraphics() {

    for (var field in $scope.school) {
      var values = [];
      for (var i = 0; i < $scope.school[field].length; i++) {
        values.push({y: $scope.school[field][i]})
      }

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
          title: {
            text: "percentual"
          }
        },
        series: [
          { 
            name: $scope.schoolName,
            data: $scope.school[field]
          },
          { 
            name: "Cidade",
            data: $scope.city[field]
          },
          { 
            name: "Estado",
            data: $scope.state[field]
          }
        ]
      });
    }
  };

  function populateInstitutionData(institution, data) {
    for (field in data) {
      institution[field] = data[field];
    }
  };


  function resetInstitutions() {
    $scope.school = {};
    $scope.city = {};
    $scope.state = {};
  };
}]);