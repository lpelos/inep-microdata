inepMicrodataApp.controller("histogramsCtrl", ["$scope", "$location", function($scope, $location) {
  
  $scope.fieldsNames = {
    ch: "Ciências Humanas",
    cn: "Ciências da Natureza",
    lc: "Líguas e Códigos",
    mt: "Matemática"
  }

  $scope.changeCity = function() {
    if ($scope.chosenCity) {
      $location.path("/escolas/" + $scope.chosenCity);
    } else {
      $location.path("/");
    }
  }

  $scope.resetInstitutions = function() {
    $scope.school = {};
    $scope.city = {};
    $scope.state = {};
  };

  $scope.resetInstitutions();

  $scope.updateChosenCity = function(code) {
    $scope.chosenCity = code;
  }

}]);