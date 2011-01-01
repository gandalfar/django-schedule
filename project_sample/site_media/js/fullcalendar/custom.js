/*
 * FCalendar 1.00
 *
 * Enjoy this software. Originally downloaded from http://www.sokati.com, 
 * check there for the latest version.
 *
 */

 var loc = '/ajax/'; // url relative to the index.html
var formStart = '<div id="dialog-form" title="Edit"><form onsubmit="return false;"><label for=name style="vertical-align:top">Title</label> <textarea name=title id=titleId cols=30>';
var formEnd = '</TEXTAREA></form></div>';

function guiCreate(start, end, allDay) {
    var id = $(formStart + formEnd);
    $(id).dialog( {
        title : 'Create',
        modal : true,
        autoOpen : true,
        lazyFetching : true,
        buttons : {
            "Ok" : function() {
                title = document.getElementById('titleId').value;
                $(id).dialog("close");
                $(id).html('');
                ev = {
                    title : title,
                    start : start.getTime() / 1000,
                    end : end.getTime() / 1000,
                    allDay : allDay
                };
                $('#calendar').fullCalendar('unselect');
                if (!title) {
                    return;
                }
                serverSave(ev);
            },
            "Cancel" : function() {
                $(id).dialog("close");
                $(id).html('');
            }
        }
    });

}

function serverSave(ev) {
    $.ajax( {
        type : 'GET',
        url : loc,
        data : 'cmd=create&title=' + ev.title + '&start=' + ev.start + '&end='
                + ev.end + '&allDay=' + ev.allDay,
        success : function(msg) {
            if (msg.length > 8) {
                $('<div>' + 'Probably location error\nid=' + msg + '</div>')
                        .dialog();
            }
            ev.id = msg;
            $('#calendar').fullCalendar('renderEvent', ev); // create
        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {
            $(
                    '<div>' + 'Error: item not saved: ' + textStatus + ' - '
                            + errorThrown + ' - ' + XMLHttpRequest + '</div>')
                    .dialog();
        }
    });
}


function guiDrop(date, allDay) {
    // retrieve the dropped element's stored Event Object
    var originalEventObject = $(this).data('eventObject');
    
    // we need to copy it, so that multiple events don't have a reference to the same object
    var ev = $.extend({}, originalEventObject);
    
    // assign it the date that was reported
    ev.start = date;
    ev.allDay = allDay;
    ev.start = ev.start.getTime() / 1000;
    ev.end = ev.start + 3600; // we just hardcode 1h timeslot for drag/drop

    $.ajax( {
        type : 'GET',
        url : loc,
        data : 'cmd=create&title=' + ev.title + '&start=' + ev.start + '&end='
                + ev.end + '&allDay=' + ev.allDay,
        success : function(msg) {
            if (msg.length > 8) {
                $('<div>' + 'Probably location error\nid=' + msg + '</div>')
                        .dialog();
            }
            ev.id = msg;
            $('#calendar').fullCalendar('renderEvent', ev); // create
        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {
            $(
                    '<div>' + 'Error: item not saved: ' + textStatus + ' - '
                            + errorThrown + ' - ' + XMLHttpRequest + '</div>')
                    .dialog();
        }
    });
}

function guiUpdateDrag(ev, dayDelta, minuteDelta, allDay, revertFunc, jsEvent,
        ui, view) {
    ev.start = ev.start.getTime() / 1000;
    ev.end = ev.end.getTime() / 1000;

    if (typeof (ev.id) == 'undefined') {// can be removed
        $('<div>ev.id is not defined...</div>').dialog();
        return;
    }

    // server update drag
    $.ajax( {
        type : 'GET',
        url : loc,
        data : 'cmd=updatePos&id=' + ev.id + '&start=' + ev.start + '&end='
                + ev.end,
        success : function(msg) {
            $('#calendar').fullCalendar('updateEvent', ev);
        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {
            $(
                    '<div>' + 'Error: item not saved: ' + textStatus + ' - '
                            + errorThrown + ' - ' + XMLHttpRequest + '</div>')
                    .dialog();
            revertFunc();
        }
    });
}

function guiUpdateClick(calEvent, jsEvent, view) {
    if (typeof (calEvent.id) == 'undefined') { // can be removed
        $('<div>ev.id is not defined...</div>').dialog();
        return;
    }
    var id = $(formStart + calEvent.title + formEnd);
    $(id).dialog( {
        title : 'Edit',
        modal : true,
        autoOpen : true,
        lazyFetching : true,
        position : 'center',
        buttons : {
            "Ok" : function() {
                textNew = document.getElementById('titleId').value;
                $(id).dialog("close");
                $(id).html('');
                serverUpdateTitle(calEvent, textNew);
            },
            "Cancel" : function() {
                $(id).dialog("close");
                $(id).html('');
            },
            "Delete" : function() {
                $(id).dialog("close");
                $(id).html('');

                var del = $('<div>Are you sure to delete this event?</div>');
                $(del).dialog( {
                    title : 'Delete',
                    modal : true,
                    autoOpen : true,
                    lazyFetching : true,
                    position : 'center',
                    buttons : {
                        "Ok" : function() {
                            $(del).dialog("close");
                            $(del).html('');
                            serverDelete(calEvent.id);
                        },
                        "Cancel" : function() {
                            $(del).dialog("close");
                            $(del).html('');
                        }
                    }
                });
            }
        }
    });
}

function serverUpdateTitle(calEvent, textNew) {
    $.ajax( {
        type : 'GET',
        url : loc,
        data : 'cmd=updateTitle&id=' + calEvent.id + '&title=' + textNew,
        success : function(msg) {
            calEvent.title = textNew;
            $('#calendar').fullCalendar('updateEvent', calEvent);
        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {
            $(
                    '<div>' + 'Error: item not saved: ' + textStatus + ' - '
                            + errorThrown + ' - ' + XMLHttpRequest + '</div>')
                    .dialog();
        }
    });
}

function serverDelete($id) {
    $.ajax( {
        type : 'GET',
        url : loc,
        data : 'cmd=delete&id=' + $id,
        success : function(msg) {
            $('#calendar').fullCalendar('removeEvents', $id);
        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {
            $(
                    '<div>' + 'Error: item not saved: ' + textStatus + ' - '
                            + errorThrown + ' - ' + XMLHttpRequest + '</div>')
                    .dialog();
        }
    });
}

$(document).ready(function() {
    $('#calendar').fullCalendar( {
        theme : true,
        header : {
            left : 'prev,next today',
            center : 'FCalendar',
            right : 'month,agendaWeek,agendaDay'
        },
        timeFormat : 'H:mm',
        axisFormat : 'H:mm',
        defaultView : 'agendaWeek',
        firstDay : 1,
        selectable : true,
        selectHelper : true,
        select : guiCreate,
        editable : true,
        droppable: true,
        drop: guiDrop,
        eventDrop : guiUpdateDrag,
        eventResize : guiUpdateDrag,
        eventClick : guiUpdateClick,
        loading : function(bool) {
            if (bool)
                $('#loading').show();
            else
                $('#loading').hide();
        },
        events : 'ajax/?cmd=read',
        defaultEventMinutes: 60
    });

    $('#datepicker').datepicker( {
        inline : true,
        firstDay : 1,
        onSelect : function(dateText, inst) {
            var d = new Date(dateText);
            $('#calendar').fullCalendar('gotoDate', d);
        },
        onChangeMonthYear : function(year, month, inst) {
            var d = new Date(year, month, 1, 0, 0, 0, 0);
            $('#calendar').fullCalendar('gotoDate', d);
        }
    });

    // Trying to change the datepicker on next/prev/today buttons, does not work
        // setDatepickerFromFullCalendar = function() {
        // var d = $('#calendar').fullCalendar('getDate');
        // $("#datepicker").datepicker("setDate", d);
        // };
        // $(".fc-button-prev").click(setDatepickerFromFullCalendar);
        // $(".fc-button-next").click(setDatepickerFromFullCalendar);
        // $(".fc-button-today").click(function() {
        // var d = new Date();
        // $('#calendar').fullCalendar('gotoDate', d);
        // $("#datepicker").datepicker("setDate", d);
        // });

    });
