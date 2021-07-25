angular.module('project_questions')

.factory('MeshService', ['$filter', '$rootScope', 'QuestionsService', function($filter, $rootScope, QuestionsService) {
    var service = {
        descriptorQuestion: null,
        qualifierQuestion: null,
    }

    service.updateQualifiers = function(set_prefix, set_index, index) {
        var value = QuestionsService.values[service.descriptorQuestion.attribute][set_prefix][set_index][index];
        var descriptors = $filter('filter')(value.items, {id: value.selected});
        if (angular.isDefined(descriptors) && descriptors && descriptors.length > 0) {
            QuestionsService.values[service.qualifierQuestion.attribute][set_prefix][set_index][index].qualifiers = descriptors[0].qualifiers;
        } else {
            QuestionsService.values[service.qualifierQuestion.attribute][set_prefix][set_index][index].qualifiers = [];
        }
    }

    return service;
}])

.controller('DescriptorController', ['$scope', 'MeshService', function($scope, MeshService) {
    var meshService = MeshService;

    $scope.init = function(question, set_prefix, set_index, index) {
        if (meshService.descriptorQuestion === null) {
            meshService.descriptorQuestion = question;
        }
    }
}])

.controller('QualifierController', ['$scope', 'MeshService', 'QuestionsService', function($scope, MeshService, QuestionsService) {
    var meshService = MeshService;

    $scope.init = function(question, set_prefix, set_index, index) {
        if (meshService.qualifierQuestion === null) {
            meshService.qualifierQuestion = question;
        }

        var value = QuestionsService.values[meshService.descriptorQuestion.attribute][set_prefix][set_index][index]
        QuestionsService.filterAutocomplete(meshService.descriptorQuestion, value).then(function() {
            $scope.$watch(function() {
                return QuestionsService.values[meshService.descriptorQuestion.attribute][set_prefix][set_index][index].selected;
            }, function() {
                meshService.updateQualifiers(set_prefix, set_index, index);
            });
        });
    }
}]);
