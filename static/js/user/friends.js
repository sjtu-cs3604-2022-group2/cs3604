

		var dataSet = [];


		$(document).ready(function(){
      
      $(".transactionButton").click(function(){
        
        row = $(this).parent().parent().parent();
        
        table.rows().deselect();
        
        table.row(row).select();
      });
		});

