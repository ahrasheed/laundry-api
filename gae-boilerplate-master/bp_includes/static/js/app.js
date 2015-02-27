(function() {
  var app = angular.module('easyLaundry', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

  app.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.useXDomain = true;
   	delete $httpProvider.defaults.headers.common['X-Requested-With'];
}])


  app.controller('LaundryItems', function($scope, $http){
  
	// Get All Item Types, Rates and Weights
  	$http.get('_ah/api/laundry_api/v1/items').success(function(data, status, headers, config) { $scope.laundryweights = data.itemlist; }).error(function(data, status, headers, config) {});	
		
	//Get All Orders
	$http.get('_ah/api/laundry_api/v1/orders').success(function(data, status, headers, config) { $scope.orders = data.orderlist; }).error(function(data, status, headers, config) {});	
	
	  $scope.orderid = 0;
	  /*$scope.orders = [
	  	{
			orderkey: 0,
			date: 'New Order',
			items: [],
			totalweight: 0,
			status: 'new'
		  },
		  {
			orderkey: 1,
			date: 'Oct 14, 2014',
			items: [
			{ name: 'Shirt', weight: 1.4, number: 4 }
			],
			totalweight: (1.4*4),
			status: 'placed'
		  },
		  {
			orderkey: 2,
			date: 'Oct 24, 2014',
			items: [],
			totalweight: 0,
			status: 'new'
		  },
		  {
			orderkey: 3,
			date: 'Nov 1, 2014',
			items: [],
			totalweight: 0,
			status: 'placed'
		  }
	  ];*/
	  
	  $scope.selectOrder = function(oid){
		$scope.orderid = oid;
	  };
	  
	  $scope.isOrder = function(oid){
		return $scope.orderid === oid;
	  };

	/*	
	 $scope.laundryweights = [
      {
        itemtype: 'Shirt',
        weight: 1.4
	  } 
    ]; */
	

    $scope.neworderItem = function(){
	
        $scope.orders[$scope.orderid].items.push({name:$scope.name.name, weight:$scope.name.weight, number:$scope.number});
        $scope.name = '';
        $scope.number = '';
		$scope.orders[$scope.orderid].totalweight = 0;
		
		for (i in $scope.orders[$scope.orderid].items){
			$scope.orders[$scope.orderid].totalweight += $scope.orders[$scope.orderid].items[i].weight * $scope.orders[$scope.orderid].items[i].number;
		}
		
    };
	
    $scope.remove=function(item){ 
	
		var index=$scope.orders[$scope.orderid].items.indexOf(item)	  
		$scope.orders[$scope.orderid].items.splice(index,1);     
	  
		$scope.orders[$scope.orderid].totalweight = 0;
		
		for (i in $scope.orders[$scope.orderid].items){
			$scope.orders[$scope.orderid].totalweight += $scope.orders[$scope.orderid].items[i].weight * $scope.orders[$scope.orderid].items[i].number;
		}
	  
    };
	
  });  
	
})();