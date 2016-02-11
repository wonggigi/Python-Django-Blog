tinyMCE.init({  
    // General options  
    mode : "textareas",  
    theme : "modern",  
    //下面使用的是插件，在新版中可以自己修改调整  
    plugins : "advlist,anchor,autolink,autosave,bbcode,charmap,code,contextmenu,directionality,emoticons,fullpage,fullscreen,hr,image,insertdatetime,layer,legacyoutput,link,lists,media,nonbreaking,noneditable,pagebreak,paste,preview,print,save,searchreplace,spellchecker,tabfocus,table,template,textcolor,visualblocks,visualchars,wordcount",  
//  
//  // Example content CSS (should be your site CSS)  
//  //content_css : "/css/style.css",  
//  
    template_external_list_url : "lists/template_list.js",  
    external_link_list_url : "lists/link_list.js",  
    external_image_list_url : "lists/image_list.js",  
    media_external_list_url : "lists/media_list.js",  
//  
    // Style formats  
    style_formats : [  
        {title : 'Bold text', inline : 'strong'},  
        {title : 'Red text', inline : 'span', styles : {color : '#ff0000'}},  
        {title : 'Help', inline : 'strong', classes : 'help'},  
        {title : 'Table styles'},  
        {title : 'Table row 1', selector : 'tr', classes : 'tablerow'}  
    ],  
   
    width: '600',  
    height: '600'  
   
});  