var sidebarForThread = new WeakMap(); //A Map is an arbitrary value for the value
var addedSideBars = new WeakMap();
var sidebarTemplatePromise = null;
var DOTURL = "https://burnham-x.appspot.com/static/images/orangedot-1.png"
var LOGOURL = "https://burnham-x.appspot.com/static/images/BurnhamXLogo.png"
var LARGELOGO = "https://burnham-x.appspot.com/static/images/BurXLarge.png"

InboxSDK.load('1', 'sdk_burnhamx_91375e9559').then(function(sdk) {

    // sdk.Search.registerSearchSuggestionsProvider(function (search) {
    //     console.log(search);

    //     return [{name:"Alex", description:"BurnhamX Searching", routeName:sdk.Router.NativeListRouteIDs.SEARCH, iconUrl:LOGOURL }];
    // });


    sdk.Router.handleListRoute(sdk.Router.NativeListRouteIDs.SEARCH, function(searchView) 
    {
        
      var query = searchView.getParams()['query']
      var table_rows = [];
      var search_results = getBurnhamXSearchResults(query, function(data){
        
        var results = data.results;
        for (var i=0; i <results.length; i++)
        {
            var tmp_thread_id = results[i]['thread_id'];
            console.log(tmp_thread_id);
            var tmp_row = {
                title: "Email Subject",
                body: "Short Snippet",
                shortDetailText: "5/5/2015",
                isRead: "false",
                labels: [{title: results[i]['opportunity']['name'] + " " + i, foregroundColor:"orange", backgroundColor:"white", iconurl: LOGOURL}],
                iconUrl: LOGOURL,
                routeID: sdk.Router.NativeRouteIDs.THREAD,
                routeParams: results[i]['thread_id']
            };
            table_rows.push(tmp_row);
        }
        var section = searchView.addCollapsibleSection({
          title: "Results from BurnhamX",
          subtitle: "Search results pertaining specifically to BurnhamX",
          tableRows: table_rows 
        }).setCollapsed(false);
      });
    
    });

    
    // the SDK has been loaded, now do something with it!
    sdk.Compose.registerComposeViewHandler(function(composeView) {

        // a compose view has come into existence, do something with it!
        composeView.addButton({
            title: "Burnham w/InboxSDK",
            iconUrl: LOGOURL,
            onClick: function(event) {
                event.composeView.insertTextIntoBodyAtCursor('Hello Burnham!');
            },
        }); 
    });


    // LIST VIEW
    sdk.Lists.registerThreadRowViewHandler(function(threadRowView) {
        var curr_id = threadRowView.getThreadID();

        // We need to replace this with an API calls
        var url = "https://burnham-x.appspot.com/association/?thread_id=" + curr_id;
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                if (data.count >= 1) {
                    addImageToThread(threadRowView, data.results[0].opportunity.name)
                }
            }
        });
    });

    sdk.Toolbars.registerToolbarButtonForList({
        title:"ASSOCIATE",
        iconUrl: LARGELOGO,
        section: "METADATA_STATE",
        onClick: function (event) {
            var selected_emails = event.selectedThreadRowViews;
            var selected_ids = "";
            for (var i=0; i<selected_emails.length; i ++)
            {
                selected_ids += selected_emails[i].getThreadID() + "_";
            }
            var send_to_api = selected_ids.substr(0, selected_ids.length-1);
            console.log(send_to_api);
            var myWindow = window.open("https://burnham-x.appspot.com/extension/bulkassociate/"+ send_to_api +"/", "Associate", "left=2000, top=100, width=400, height=400, titlebar=no ,menubar=no");
            },
    });


    sdk.Toolbars.registerToolbarButtonForThreadView(
    {
            title:"ASSOCIATE",
            iconUrl: LARGELOGO,
            section: "METADATA_STATE",
            onClick: function (event) {
                thread_id = event.threadView.getThreadID();
                console.log(event.threadView.getMessageViews());
                var myWindow = window.open("https://burnham-x.appspot.com/extension/associate/"+ thread_id +"/", "Associate", "left=2000, top=100, width=400, height=400, titlebar=no ,menubar=no");
            },
        });

    sdk.Conversations.registerThreadViewHandler(function(threadView) {
        console.log(threadView);
        var url = "https://burnham-x.appspot.com/association/?thread_id=" + threadView.getThreadID();

        $.ajax({
            url: url,
            type: "GET",
            success: function(data) { //
                if (data.count >= 1) {
                    $.ajax({
                        
                        url: "https://burnham-x.appspot.com/opportunity/" + data.results[0].opportunity.id + "/",
                        type: "GET",
                        success: function(oppData) {
                            console.log(oppData);
                            addAssociatedSideBar(threadView, oppData);
                        }
                    });
                }
                else
                {
                      addNewAssociationSideBar(threadView);                  
                }
            }
        });
    });

});


function getBurnhamXSearchResults(query, callback)
{
    var url = "https://burnham-x.appspot.com/association/?search=" + query;
    $.ajax({
            url: url,
            type: "GET",
            success: callback
        });
}


function addNewAssociationSideBar(threadView)
{
    if (!sidebarForThread.has(threadView)) {
        sidebarForThread.set(threadView, document.createElement('div'));

        var sideBar = threadView.addSidebarContentPanel({
            el: sidebarForThread.get(threadView),
            title: "BurnhamX",
            iconUrl: LARGELOGO
        });
        addedSideBars.set(threadView, sideBar);
    }
    var source = '<div class="column"><h3>Not Associated</h3>Click the <img src="' +  LOGOURL +'"> icon on the navigation bar to associate</div>';
    var template = Handlebars.compile(source);
    var context = {};
    var html = template(context);
    sidebarForThread.get(threadView).innerHTML = sidebarForThread.get(threadView).innerHTML + html;
}



function addImageToThread(threadRowView, name) {
    threadRowView.addImage({
        imageUrl: DOTURL,
        tooltip: name,
    });
}

function addAssociatedSideBar(threadView, oppData) {
    if (!sidebarForThread.has(threadView)) {
        sidebarForThread.set(threadView, document.createElement('div'));

        threadView.addSidebarContentPanel({
            el: sidebarForThread.get(threadView),
            title: "BurnhamX",
            iconUrl: LARGELOGO
        });
    }


    var source = '<div class="column"><h4>Association Found</h4>OPTY: {{name}} <br />Address: {{address}}<br /></div>';
    var template = Handlebars.compile(source);
    var context = {
        name: oppData.name,
        address: oppData.street + " " + oppData.city + ", "+oppData.state
    };

    var html = template(context);
    sidebarForThread.get(threadView).innerHTML = sidebarForThread.get(threadView).innerHTML + html;
}

function isAssociated(threadID)
{
    var url = "https://burnham-x.appspot.com/association/?thread_id=" + threadID;
    return $.ajax({
        url: url,
        type: "GET",   
        async: false,        
        success: function(data) { //
            console.log(data);
            }
        
    });    

}
function getHtml(e){
    return "<h3>hey</h3>";
}
