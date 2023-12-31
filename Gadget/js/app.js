var sidebarForThread = new WeakMap(); //A Map is an arbitrary value for the value
var sidebarTemplatePromise = null;
var LOGOURL = "https://burnham-x.appspot.com/static/images/BEye.png"
InboxSDK.load('1', 'sdk_burnhamx_91375e9559').then(function(sdk) {


    // the SDK has been loaded, now do something with it!
    sdk.Compose.registerComposeViewHandler(function(composeView) {

        // a compose view has come into existence, do something with it!
        composeView.addButton({
            title: "Burnham w/InboxSDK",
            iconUrl: 'images/BEye.png',
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
                    addImageToThread(threadRowView)
                }
            }
        });
    });

    sdk.Toolbars.registerToolbarButtonForList({
        title:"ASSOCIATE",
        iconUrl: LOGOURL,
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
            iconUrl: LOGOURL,
            section: "METADATA_STATE",
            onClick: function (event) {
                thread_id = event.threadView.getThreadID();
                console.log(thread_id);
                var myWindow = window.open("https://burnham-x.appspot.com/extension/associate/"+ thread_id +"/", "Associate", "left=2000, top=100, width=400, height=400, titlebar=no ,menubar=no");
            },
        });

    sdk.Conversations.registerMessageViewHandler(function(messageView) {

        var threadView = messageView.getThreadView();
        //console.log(threadView);

        var url = "https://burnham-x.appspot.com/association/?thread_id=" + threadView.getThreadID();
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) { //
                if (data.count >= 1) {
                    $.ajax({
                        url: "https://burnham-x.appspot.com/opportunity/" + data.results[0].opportunity + "/",
                        type: "GET",
                        success: function(oppData) {
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


function addNewAssociationSideBar(threadView)
{
    if (!sidebarForThread.has(threadView)) {
        sidebarForThread.set(threadView, document.createElement('div'));

        threadView.addSidebarContentPanel({
            el: sidebarForThread.get(threadView),
            title: "BurnhamX",
            iconUrl: chrome.runtime.getURL('images/BEye.png')
        });
    }
    var source = '<div class="column"><h3>Not Associated</h3>Click the <img src="' +  LOGOURL +'"> icon on the navigation bar to associate</div>';
    var template = Handlebars.compile(source);
    var context = {};
    var html = template(context);
    sidebarForThread.get(threadView).innerHTML = sidebarForThread.get(threadView).innerHTML + html;
}



function addImageToThread(threadRowView) {
    threadRowView.addImage({
        imageUrl: chrome.runtime.getURL("images/BEye.png"),
        tooltip: "Associated",
    });
}

function addAssociatedSideBar(threadView, oppData) {
    if (!sidebarForThread.has(threadView)) {
        sidebarForThread.set(threadView, document.createElement('div'));

        threadView.addSidebarContentPanel({
            el: sidebarForThread.get(threadView),
            title: "BurnhamX",
            iconUrl: chrome.runtime.getURL('images/BEye.png')
        });
    }


    var source = '<div class="column"><h4>Association Found</h4>Customer: {{name}} <br />Address: {{address}}<br /></div>';
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
function getHtml(){
    return "<h3>hey</h3>";
}
