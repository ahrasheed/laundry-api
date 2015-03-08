(function() {
  var app = angular.module('easyLaundry', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

  app.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.useXDomain = true;
   	delete $httpProvider.defaults.headers.common['X-Requested-With'];
}])

	app.controller('LaundryItems', function($scope, $http, $timeout){  
		
		$scope.successTextAlert = "Empty content";
		$scope.showSuccessAlert = false;

		$scope.switchBool = function(value) {
		$scope[value] = !$scope[value];
	};  

    //$scope.initialize = function(){	
	// Get All Item Types, Rates and Weights
  	$http.get('_ah/api/laundry_api/v1/items').success(function(data, status, headers, config) { $scope.laundryweights = data.itemlist; }).error(function(data, status, headers, config) {});	
			
	$scope.orders = [{  ordercounter: 0, tabname:"New Order", comments:"New Order", items: [] }];	//var ar3 = ar1.concat(ar2);
	//Get All Orders
	$http.get('_ah/api/laundry_api/v1/orders').success(function(data, status, headers, config) { $scope.orders = $scope.orders.concat(data.orderlist); }).error(function(data, status, headers, config) {});	
	
	//};
	
//	timeout( function(){ $scope.initialize(); }, 1000);
	
	  $scope.orderid = 0;
	  /*$scope.orders = [
	  	{
			orderkey: 0,
			date: 'New Order',
			items: [],
			totalweight: 0,
			status: 'new'
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
	
        $scope.orders[$scope.orderid].items.push({name:$scope.name.name, weight:$scope.name.weight, itemkey:$scope.name.itemkey, number:$scope.number});
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
	
	//$scope.orderform = {comments: "Asad"};

   $scope.placeorder=function(item){	
		//$scope.orders = [{  ordercounter: 0, tabname:"New Order", items: [] }];
		$http.post('_ah/api/laundry_api/v1/placeorder', $scope.orders[0]).success(function(data, status, headers, config) { $scope.showSuccessAlert = true; $scope.successTextAlert = "Order Placed"; 
					
			$scope.orders = [{  ordercounter: 0, comments:"New Order", tabname:"New Order", items: [] }];	//var ar3 = ar1.concat(ar2);
			//Get All Orders
			$http.get('_ah/api/laundry_api/v1/orders').success(function(data, status, headers, config) { $scope.orders = $scope.orders.concat(data.orderlist); }).error(function(data, status, headers, config) {});	
		
		}).error(function(data, status, headers, config) { });
		

    };
	
	
  });  
	
})();