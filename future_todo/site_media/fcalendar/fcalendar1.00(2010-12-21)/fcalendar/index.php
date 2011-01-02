<?php
/*
 * FCalendar 1.00
 *
 * Enjoy this software. Originally downloaded from http://www.sokati.com, 
 * check there for the latest version.
 *
 */

include_once 'Database.php';
include_once 'Event.php';

error_reporting ( E_ALL );
//error_log ( 'start _get=' . print_r ( $_GET, true ) . "\n", 3, '_errors.txt' );


try {
	if (! isset ( $_GET ['cmd'] )) {
		throw new Exception ( 'cmd is not set' );
	}
	$server = 'localhost';
	if (strpos ( $_SERVER ['SERVER_NAME'], 'localhost' ) !== false) {
		$user = 'fcalendar'; // FILL IN YOURSELF
		$password = 'fcalendar'; // FILL IN YOURSELF
		$database = 'fcalendar'; // FILL IN YOURSELF
	} else {
		$user = 'fcalendar'; // FILL IN YOURSELF
		$password = 'fcalendar'; // FILL IN YOURSELF
		$database = 'fcalendar'; // FILL IN YOURSELF
	}
	if ($user == '') {
		throw new Exception ( 'Setup fcalendar by adjusting index.php.' );
	}
	$database = new Database ( $server, $user, $password, $database );
	$eventDb = new Event ( $database );
	switch ($_GET ['cmd']) {
		case 'create' :
			echo $eventDb->create ( $_GET ['title'], $_GET ['start'], $_GET ['end'], $_GET ['allDay'] );
			break;
		case 'updatePos' :
			$eventDb->updatePos ( $_GET ['id'], $_GET ['start'], $_GET ['end'] );
			break;
		case 'updateTitle' :
			$eventDb->updateTitle ( $_GET ['id'], $_GET ['title'] );
			break;
		case 'delete' :
			$eventDb->delete ( $_GET ['id'] );
			break;
		case 'read' :
			$events = $eventDb->read ( $_GET ['start'], $_GET ['end'] );
			$result = json_encode ( $events );
			
			// json does not parse booleans without quotes, and reads the boolean as string 0 and string 1
			$result = str_replace ( '"allDay":"0"', '"allDay":false', $result );
			$result = str_replace ( '"allDay":"1"', '"allDay":true', $result );
			
			echo $result;
			break;
	}
} catch ( Exception $ex ) {
	error_log ( 'Exception: ' . $ex, 3, '_errors.txt' );
}

?>
