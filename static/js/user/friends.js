

		var dataSet = [{"ID":7,"Age":31,"FirstName":"Sam","LastName":"Verber","Email":"sam@verber.org","Balance":2.25},{"ID":2,"Age":32,"FirstName":"John","LastName":"Smith","Email":"john@smith.com","Balance":12.5},{"ID":22,"Age":29,"FirstName":"Dawn","LastName":"Skye","Email":"dawn@sky.com","Balance":12.5},{"ID":26,"Age":39,"FirstName":"Jeremy","LastName":"Fisher","Email":"jeremy@fisher.co","Balance":12.5},{"ID":14,"Age":23,"FirstName":"Dan","LastName":"Dare","Email":"dan@dare.net","Balance":12.5},{"ID":3,"Age":27,"FirstName":"Frank","LastName":"Doland","Email":"frank@doland.com","Balance":22.5},{"ID":9,"Age":45,"FirstName":"Grace","LastName":"Sloane","Email":"grace@sloane.io","Balance":22.5},{"ID":27,"Age":51,"FirstName":"James","LastName":"Bond","Email":"james@bond.uk","Balance":22.5},{"ID":21,"Age":25,"FirstName":"Jerry","LastName":"Can","Email":"jerry@can.co","Balance":22.5},{"ID":4,"Age":18,"FirstName":"Pink","LastName":"Sky","Email":"pink@sky.io","Balance":27.5},{"ID":8,"Age":25,"FirstName":"Fay","LastName":"White","Email":"fay@white.net","Balance":27.5},{"ID":16,"Age":63,"FirstName":"Joshua","LastName":"Jacobson","Email":"joshua@jacobson.net","Balance":27.5},{"ID":28,"Age":46,"FirstName":"Prince","LastName":"Igor","Email":"prince@igor.pl","Balance":27.5},{"ID":5,"Age":54,"FirstName":"Adam","LastName":"Aardvark","Email":"adam@aardvark.com","Balance":6.3},{"ID":25,"Age":49,"FirstName":"Mickey","LastName":"Mouse","Email":"mickey@mouse.usa","Balance":6.3},{"ID":10,"Age":76,"FirstName":"Placido","LastName":"Agnescu","Email":"placido@agnescu.com","Balance":6.3},{"ID":15,"Age":37,"FirstName":"James","LastName":"Pickering","Email":"james@pickering.pl","Balance":6.3},{"ID":20,"Age":22,"FirstName":"Sultana","LastName":"Pasa","Email":"sultana@pasa.es","Balance":6.3},{"ID":6,"Age":67,"FirstName":"Ira","LastName":"Goose","Email":"ira@goose.com","Balance":2.8},{"ID":18,"Age":43,"FirstName":"John","LastName":"Doe","Email":"john@doe.com","Balance":2.8},{"ID":12,"Age":57,"FirstName":"Hart","LastName":"Wolff","Email":"hart@wolff.de","Balance":2.8},{"ID":24,"Age":36,"FirstName":"Donald","LastName":"Duck","Email":"donald@duck.cz","Balance":2.8}];


		$(document).ready(function(){
			table = $('#usertable').DataTable({
        		data: dataSet,
				columns: [
					{ data: "ID" },
					{ data: null, "defaultContent":	"<div class='btn-group dropright'>"+
														"<button type='button' class='btn btn-primary btn-sm transactionButton' data-toggle='dropdown'>取消关注</button>"+
													"</div>"
					},
					{ data: "Age" },
					{ data: "FirstName" },
                    { data: null, "defaultContent":	"男"
                },
					{ data: null, "defaultContent":	"<img class = 'avatar'  src = 'https://ts1.cn.mm.bing.net/th?id=OIP-C.JPaFw0vH2f6Qy44aUfZ4jgAAAA&w=150&h=150&c=8&rs=1&qlt=90&o=6&dpr=1.6&pid=3.1&rm=2' alt = ''>"
					},

					{ data: "Balance" }
				],
				"order": [2, "asc"],
        /*select: {
            style:    'single',
            selector: 'td:first-child'
        },*/
				"info": false
			});
      
      $(".transactionButton").click(function(){
        
        row = $(this).parent().parent().parent();
        
        table.rows().deselect();
        
        table.row(row).select();
      });
		});

