inepMicrodataApp.controller("histogramsCtrl", ["$scope", "$location", function($scope, $location) {
  $scope.schools = schools;

  $scope.selectedSchool = null;
  $scope.$watch("selectedSchool", function() {
    if ($scope.schools[$scope.selectedSchool]) {
      $scope.changeSchool($scope.schools[$scope.selectedSchool]);
    }
  });

  $scope.schoolNames = [];
  for (var schoolName in schools) {
    $scope.schoolNames.push(schoolName);
  }

  $scope.fieldsNames = {
    ch: "Ciências Humanas",
    cn: "Ciências da Natureza",
    lc: "Líguas e Códigos",
    mt: "Matemática"
  }

  $scope.changeSchool = function(schoolCode) {
    schoolCode = schoolCode || $scope.selectedSchool;
    if (schoolCode) {
      $location.path("/escolas/" + schoolCode);
    }
  }

  $scope.resetInstitutions = function() {
    $scope.school = {};
    $scope.city = {};
    $scope.state = {};
  };

  $scope.updateSelectedSchool = function(code) {
    $scope.selectedSchool = code;
  }

  $scope.resetInstitutions();

}]);