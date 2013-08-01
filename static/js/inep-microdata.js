inepMicrodataApp = angular.module("inepMicrodata", ["ngResource"]).

  config(["$routeProvider", function($routeProvider) { 
    var graphicsConfig = {
      templateUrl: "/static/templates/graphics.html",
      controller: "graphicsCtrl"
    }

    $routeProvider.when("/escolas/:schoolCode", graphicsConfig).

    when("/schools/:schoolCode", graphicsConfig)

  }])

  .directive('autoComplete', ["$timeout", function($timeout) {
      return function(scope, iElement, iAttrs) {
        iElement.autocomplete({
          source: scope[iAttrs.uiItems],
          select: function() {
            $timeout(function() {
              iElement.trigger('input');
            }, 0);
          }
        });
      };
  }]);