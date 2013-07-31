inepMicrodataApp = angular.module("inepMicrodata", ["ngResource"]).

  config(["$routeProvider", function($routeProvider) { 
    var graphicsConfig = {
      templateUrl: "/static/templates/graphics.html",
      controller: "graphicsCtrl"
    }

    $routeProvider.when("/escolas/:schoolCode", graphicsConfig).

    when("/schools/:schoolCode", graphicsConfig)

  }]);