(function() {
  var app = angular.module('easyLaundry', []);

  app.controller('LaundryItems', function($scope){
  
	  $scope.orderid = 0;
	  $scope.orders = [
	  	{
			id: 0,
			date: 'New Order',
			orderitems: [],
			totalweight: 0,
			status: 'new'
		  },
		  {
			id: 1,
			date: 'Oct 14, 2014',
			orderitems: [
			{ name: 'Shirt', weight: 1.4, quantity: 4 }
			],
			totalweight: (1.4*4),
			status: 'placed'
		  },
		  {
			id: 2,
			date: 'Oct 24, 2014',
			orderitems: [],
			totalweight: 0,
			status: 'new'
		  },
		  {
			id: 3,
			date: 'Nov 1, 2014',
			orderitems: [],
			totalweight: 0,
			status: 'placed'
		  }
	  ];
	  
	  $scope.selectOrder = function(oid){
		$scope.orderid = oid;
	  };
	  
	  $scope.isOrder = function(oid){
		return $scope.orderid === oid;
	  };
	
	  $scope.laundryweights = [
      {
        itemtype: 'Shirt',
        weight: 1.4
	  },
      {
        itemtype: 'Trouser',
        weight: 2.3
	  },
      {
        itemtype: 'Underwear',
        weight: 0.4
	  },	  
      {
        itemtype: 'Bra',
        weight: 0.5
	  },	
      {
        itemtype: 'Socks',
        weight: 0.2
	  },
      {
        itemtype: 'Waist',
        weight: 0.3
	  }		  
    ]; 
	

    $scope.neworderItem = function(){
	
        $scope.orders[$scope.orderid].orderitems.push({name:$scope.name.itemtype, weight:$scope.name.weight, quantity:$scope.quantity});
        $scope.name = '';
        $scope.quantity = '';
		$scope.orders[$scope.orderid].totalweight = 0;
		
		for (i in $scope.orders[$scope.orderid].orderitems){
			$scope.orders[$scope.orderid].totalweight += $scope.orders[$scope.orderid].orderitems[i].weight * $scope.orders[$scope.orderid].orderitems[i].quantity;
		}
		
    };
	
    $scope.remove=function(item){ 
	
		var index=$scope.orders[$scope.orderid].orderitems.indexOf(item)	  
		$scope.orders[$scope.orderid].orderitems.splice(index,1);     
	  
		$scope.orders[$scope.orderid].totalweight = 0;
		
		for (i in $scope.orders[$scope.orderid].orderitems){
			$scope.orders[$scope.orderid].totalweight += $scope.orders[$scope.orderid].orderitems[i].weight * $scope.orders[$scope.orderid].orderitems[i].quantity;
		}
	  
    };
	
  });  
	
})();