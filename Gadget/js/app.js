var sidebarForThread = new WeakMap(); //A Map is an arbitrary value for the value
var addedSideBars = new WeakMap();
var cache = {}
var sidebarTemplatePromise = null;
var DOTURL = "https://burnham-x.appspot.com/static/images/orangedot-1.png"
var LOGOURL = "https://burnham-x.appspot.com/static/images/BurnhamXLogo.png"
var LARGELOGO = "https://burnham-x.appspot.com/static/images/BurXLarge.png"

InboxSDK.load('1', 'sdk_burnhamx_91375e9559').then(function(sdk) {
    // LIST VIEW
    sdk.Lists.registerThreadRowViewHandler(function(threadRowView) {
        var curr_id = threadRowView.getThreadID();

        // We need to replace this with an API calls
        var url = "https://burnham-x.appspot.com/association/?thread_id=" + curr_id;

        if (curr_id in cache)
        {
            addImageToThread(threadRowView, cache[curr_id])
        }
        else
        {
            $.ajax({
                url: url,
                beforeSend: function (xhr){
                    xhr.setRequestHeader("Authorization", "Token d0de5a3282b98955e158911efef5a8c16ec81607");
                },
                type: "GET",
                success: function(data) {
                    if (data.count >= 1) {
                        addImageToThread(threadRowView, data.results[0].opportunity.name)
                        cache[curr_id] = data.results[0].opportunity.name
                    }
                }
            });
        }
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
                message_id = event.threadView.getMessageViews()[0].getMessageID()
                var myWindow = window.open("https://burnham-x.appspot.com/extension/associate/"+ thread_id +"/" + message_id +"/", "Associate", "left=2000, top=100, width=400, height=400, titlebar=no ,menubar=no");
            },
        });

    sdk.Conversations.registerMessageViewHandler(function(messageView) {
        // This call will be fired when the message is expaned for the first time
        if (messageView.getViewState() == "EXPANDED")
        {
            //addSideBarForMessage(messageView.getMessageID(), messageView.getThreadView());
            var message_id = messageView.getMessageID();
            var thread_id = messageView.getThreadView().getThreadID();
            $.ajax({
                url: "https://burnham-x.appspot.com/extension/future/?message_id=" + message_id +  "&thread_id=" + thread_id,
                type:'GET'
            })
        }
        // This is triggered when a particular message is re-expanded.
        messageView.on('viewStateChange', function(event) {
            console.log(event);
            //addSideBarForMessage(event.messageView.getMessageID(), event.messageView.getThreadView());
        })
    });

    sdk.Conversations.registerThreadViewHandler(function(threadView) {
        
        var url = "https://burnham-x.appspot.com/association/?active=true&thread_id=" + threadView.getThreadID();

        $.ajax({
            url: url,
            beforeSend: function (xhr){
                xhr.setRequestHeader("Authorization", "Token d0de5a3282b98955e158911efef5a8c16ec81607");
            },
            type: "GET",
            success: function(data) { //
                if (data.count >= 1) {
                    $.ajax({
                        beforeSend: function (xhr){
                            xhr.setRequestHeader("Authorization", "Token d0de5a3282b98955e158911efef5a8c16ec81607");
                        },
                        url: "https://burnham-x.appspot.com/opportunity/" + data.results[0].opportunity.id + "/",
                        
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


function getBurnhamXSearchResults(query, callback)
{
    var url = "https://burnham-x.appspot.com/association/?search=" + query;
    $.ajax({
            url: url,
            beforeSend: function (xhr){
                xhr.setRequestHeader("Authorization", "Token d0de5a3282b98955e158911efef5a8c16ec81607");
            },
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

    // This is ugly!
    var source = '<div class="column"><h3>No Association Found</h3>Click below to associate <input type="image" src="' + LOGOURL + '" onclick="window.open(\'{{url}}\', \'Associate\', \'left=2000, top=100, width=400, height=400, titlebar=no ,menubar=no\')"></div>';
    var template = Handlebars.compile(source);
    var context = {
        url: "https://burnham-x.appspot.com/extension/associate/"+ threadView.getThreadID() +"/" + threadView.getMessageViews()[0].getMessageID() + "/"
    };
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
    var source = '<div class="column"><h4>Association Found</h4><b>OPTY:</b> {{name}} <br /><br /><b>Address:</b> {{address}}<br /></div>';
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
