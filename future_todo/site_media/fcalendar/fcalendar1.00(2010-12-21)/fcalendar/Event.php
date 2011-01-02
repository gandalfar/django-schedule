<?php
/*
 * FCalendar 1.00
 *
 * Enjoy this software. Originally downloaded from http://www.sokati.com, 
 * check there for the latest version.
 *
 */

class Event {
	
	private $database;
	
	public function __construct(Database $database) {
		$this->database = $database;
		if (! $database->getTableExists ( 'event' )) {
			$sql = 'CREATE TABLE event (
			id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT, PRIMARY KEY(id),
			title varchar(192) NOT NULL,
			start INT UNSIGNED,
			end INT UNSIGNED,
			allDay bool,
			description varchar(128)
			) CHARSET=utf8 COLLATE=utf8_unicode_ci';
			$result = mysql_query ( $sql, $database->getHandle () );
			if ($result == FALSE) {
				throw new Exception ( 'Could not create table, sql=' . $sql );
			}
		}
	}
	
	public function create($title, $start, $end, $allDay) {
		$title = Database::sqlInjectPrevent ( $title );
		$start = Database::sqlInjectPrevent ( $start );
		$end = Database::sqlInjectPrevent ( $end );
		$allDay = Database::sqlInjectPrevent ( $allDay );
		
		if ($allDay == 'true') {
			$allDay = '1';
		} else {
			$allDay = '0';
		}
		
		$query = "INSERT INTO event (title,start,end,allDay) VALUES
			('" . $title . "','" . $start . "','" . $end . "','" . $allDay . "')";
		$result = mysql_query ( $query, $this->database->getHandle () );
		if ($result == FALSE) {
			throw new Exception ( 'error in sql=' . $query );
		}
		$query = 'select id from event where title=\'' . $title . '\' and start=\'' . $start . '\' and
			end=\'' . $end . '\' and allDay=\'' . $allDay . '\'';
		$returner = Database::selectQuery ( $query, $this->database );
		if (count ( $returner ) == 0) {
			throw new Exception ( 'create(): no id found for title=' . $title . ' start=' . $start . ' end=' . $end . ' allDay=' . $allDay );
		}
		return $returner [0] ['id'];
	}
	
	public function read($start, $end) {
		$start = Database::sqlInjectPrevent ( $start );
		$end = Database::sqlInjectPrevent ( $end );
		$query = 'select * from event where not (start>=' . $end . ' or end<=' . $start . ')';
		return Database::selectQuery ( $query, $this->database );
	}
	
	public function delete($id) {
		$id = Database::sqlInjectPrevent ( $id );
		$query = 'delete from event where id=' . $id;
		return Database::selectQuery ( $query, $this->database );
	}
	
	public function updatePos($id, $start, $end) {
		$id = Database::sqlInjectPrevent ( $id );
		$start = Database::sqlInjectPrevent ( $start );
		$end = Database::sqlInjectPrevent ( $end );
		
		$query = 'UPDATE event SET start=' . $start . ',end=' . $end . ' WHERE id=' . $id . ' LIMIT 1';
		$result = mysql_query ( $query, $this->database->getHandle () );
		if ($result == FALSE) {
			throw new Exception ( 'error in sql=' . $query );
		}
	}
	
	public function updateTitle($id, $title) {
		$id = Database::sqlInjectPrevent ( $id );
		$title = Database::sqlInjectPrevent ( $title );
		
		$query = 'UPDATE event SET title=\'' . $title . '\' WHERE id=' . $id . ' LIMIT 1';
		$result = mysql_query ( $query, $this->database->getHandle () );
		if ($result == FALSE) {
			throw new Exception ( 'error in sql=' . $query );
		}
	}

} // end of class


?>