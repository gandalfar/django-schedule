<?php
/*
 * FCalendar 1.00
 *
 * Enjoy this software. Originally downloaded from http://www.sokati.com, 
 * check there for the latest version.
 *
 */

class Database {
	
	private $sqlConn;
	
	private $sql_host, $sql_user, $sql_password, $sql_database;
	
	public function __construct($sql_host, $sql_user, $sql_password, $sql_database) {
		$this->sql_host = $sql_host;
		$this->sql_user = $sql_user;
		$this->sql_password = $sql_password;
		$this->sql_database = $sql_database;
	}
	
	public function __destruct() {
		if (isset ( $this->sqlConn )) {
			mysql_close ( $this->sqlConn );
		}
	}
	
	public function getHandle() {
		if (! isset ( $this->sqlConn )) {
			$this->sqlConn = mysql_connect ( $this->sql_host, $this->sql_user, $this->sql_password );
			if ($this->sqlConn == FALSE) {
				throw new Exception ( 'Could not connect to the database' );
			}
			$selected = mysql_select_db ( $this->sql_database );
			if ($selected == FALSE) {
				throw new Exception ( 'Could not select the database' );
			}
			mysql_query ( 'SET NAMES \'utf8\'' );
		}
		return $this->sqlConn;
	}
	
	public function getTableExists($table) {
		// or in a method: http://forums.mysql.com/read.php?101,112346,219132#msg-219132
		$sql = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=\'' . $this->sql_database . "' AND table_name='" . $table . "'";
		$result = mysql_query ( $sql, $this->getHandle () );
		if (! $result) {
			throw new Exception ( 'Error in query=' . $sql );
		}
		$row = mysql_fetch_row ( $result );
		return $row [0] == '1';
	}
	
	public static function sqlInjectPrevent($value, $silent = false) {
		if (is_array ( $value )) {
			if ($silent) {
				die ();
			}
			throw new Exception ( 'cannot trim, is array: ' . print_r ( $value, true ) );
		}
		if (strlen ( $value ) > 512) {
			if ($silent) {
				die ();
			}
			throw new Exception ( 'value way too long: ' . substr ( $value, 0, 64 ) );
		}
		// Note: strstr is because otherwise we are unnecessarely spending time
		// and memory on creating new strings, and most often these things do not
		// occur. We repladce with a space so that you cannot make a string with
		// these and then comply to the minimal length check before database-
		// calls, but not apply to these in reality.
		if (strstr ( $value, "'" ) != false) {
			$value = str_replace ( "'", ' ', $value );
		}
		if (strstr ( $value, ';' ) != false) {
			$value = str_replace ( ';', ' ', $value );
		}
		if (strstr ( $value, '"' ) != false) {
			$value = str_replace ( '"', ' ', $value );
		}
		if (strstr ( $value, '`' ) != false) {
			$value = str_replace ( '`', ' ', $value );
		}
		if (strstr ( $value, '<' ) != false) {
			$value = str_replace ( '<', ' ', $value );
		}
		if (strstr ( $value, '>' ) != false) {
			$value = str_replace ( '>', ' ', $value );
		}
		if (strstr ( $value, '&' ) != false) {
			$value = str_replace ( '>', ' ', $value );
		}
		// Disabled because texts must be able to contain enters,
		// AND it doesn't work by only replacing \n with a space,
		// it only introduces spaces.
		//		if (strstr ( $value, "\n" ) != false) {
		//			$value = str_replace ( "\n", ' ', $value );
		//		}
		return trim ( $value );
	}
	
	public static function selectQuery($sql, $database) {
		//				if (Index::getDebug ()) {
		//					echo '<font color=purple>' , $sql , '</font><br>';
		//				}
		

		$result = mysql_query ( $sql, $database->getHandle () );
		if (! $result) {
			throw new Exception ( 'Error in query=' . $sql );
		}
		$returner = array ();
		while ( true ) {
			$row = mysql_fetch_assoc ( $result );
			if ($row == false) {
				break;
			}
			$returner [] = $row;
		}
		mysql_free_result ( $result );
		return $returner;
	}
	
} // end of class


?>