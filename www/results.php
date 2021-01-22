<?php
echo '<style>
body {
  background-color: black;
}
</style>';
include("classes/tmfcolorparser.inc.php");
$cp = new TMFColorParser();

function formatTime ($MwTime, $tsec = true) {

		if ($MwTime > 0) {
			$tseconds = ((strlen($MwTime) > 3) ? substr($MwTime, strlen($MwTime)-3) : $MwTime);
			$MwTime = floor($MwTime / 1000);
			$hours = floor($MwTime / 3600);
			$MwTime = $MwTime - ($hours * 3600);
			$minutes = floor($MwTime / 60);
			$MwTime = $MwTime - ($minutes * 60);
			$seconds = floor($MwTime);
			if ($tsec) {
				if ($hours) {
					return sprintf('%d:%02d:%02d.%03d', $hours, $minutes, $seconds, $tseconds);
				}
				else {
					return sprintf('%d:%02d.%03d', $minutes, $seconds, $tseconds);
				}
			}
			else {
				if ($hours) {
					return sprintf('%d:%02d:%02d', $hours, $minutes, $seconds);
				}
				else {
					return sprintf('%d:%02d', $minutes, $seconds);
				}
			}
		}
		else {
			return '0:00:000';
		}
	}
echo '<br>';	
// 1st Map
$data = array();
$link = mysqli_connect("host", "user", "password", "pyplanet", "3306");
if (!$link) {
    echo "Error: Unable to connect to MySQL." . PHP_EOL;
    echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

$MapRequest = "SELECT *
FROM `map`
WHERE `id` =1"; //

$result = mysqli_query($link, $MapRequest);

if (!$result) {
    $message  = "Invalid query: " . mysqli_connect_error() . "\n";
    $message .= "Whole query: " . $MapRequest;
    die($message);
}

$Mapname = '$fffMapName: &nbsp; &nbsp; &nbsp;';
while($row = mysqli_fetch_array($result)) {
	$MapColor = '$fff'.$row[4].'';
  echo "".$cp->toHTML($Mapname)."".$cp->toHTML($MapColor)."".$row[4]."";
  echo '<br>';
}

$RecordRequest = "SELECT * FROM player INNER JOIN match_results ON match_results.player_id = player.id Where match_results.map_id=1 ORDER BY match_results.rank ASC";

$result = mysqli_query($link, $RecordRequest);

if (!$result) {
    $message  = "Invalid query: " . mysqli_connect_error() . "\n";
    $message .= "Whole query: " . $RecordRequest;
    die($message);
}

	echo '<table width=\"100%\" border=\"0\" align=\"center\">
  <tr">
    <td width=\"60\" class=\"tablehead\" bgcolor="#FFFFF">Rank</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Nickname</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Time</td>
	<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">TimeDifference</td>
    <td width=\"80\" class=\"tablehead\" bgcolor="#FFFFF">Points</td>
</td>';

$rank = 0;
$points = array();
$array_result = array();
$pointsmap = array();

while ($row = mysqli_fetch_array($result)) {
$array_result[] = $row;
$rank++;
$bestTime = $array_result[0]['bestracetime'];
$timeDiff = $row['bestracetime'] - $bestTime;
$format_timeDiff = formatTime($timeDiff, true);
$time = formatTime($row['bestracetime'], true);
$points = $array_result[0]['map_points'];
$pointsmap[] = array('nick' => $row['nickname'],'totalpoints' => +$points);

		echo "<tr>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$rank."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$row['nickname']."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$time."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">+".$format_timeDiff."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$points."</td>";
		echo "</tr>";
}
echo'</table>';
echo '<br>';
//2nd Map
$link = mysqli_connect("host", "user", "password", "pyplanet", "3306");
if (!$link) {
    echo "Error: Unable to connect to MySQL." . PHP_EOL;
    echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

$MapRequest = "SELECT *
FROM `map`
WHERE `id` =1";

$result = mysqli_query($link, $MapRequest);

if (!$result) {
    $message  = "Invalid query: " . mysqli_connect_error() . "\n";
    $message .= "Whole query: " . $MapRequest;
    die($message);
}

$Mapname = '$fffMapName: &nbsp; &nbsp; &nbsp;';
while($row = mysqli_fetch_array($result)) {
	$MapColor = '$fff'.$row[4].'';
  echo "".$cp->toHTML($Mapname)."".$cp->toHTML($MapColor)."".$row[4]."";
  echo '<br>';
}

$RecordRequest = "SELECT * FROM player INNER JOIN match_results ON match_results.player_id = player.id Where match_results.map_id=1 ORDER BY match_results.rank ASC";

$result = mysqli_query($link, $RecordRequest);

if (!$result) {
    $message  = "Invalid query: " . mysqli_connect_error() . "\n";
    $message .= "Whole query: " . $RecordRequest;
    die($message);
}

	echo '<table width=\"100%\" border=\"0\" align=\"center\">
  <tr">
    <td width=\"60\" class=\"tablehead\" bgcolor="#FFFFF">Rank</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Nickname</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Time</td>
	<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">TimeDifference</td>
    <td width=\"80\" class=\"tablehead\" bgcolor="#FFFFF">Points</td>
</td>';

$rank = 0;
$points = array();
$array_result = array();
$pointsmap = array();

while ($row = mysqli_fetch_array($result)) {
$array_result[] = $row;
$rank++;
$bestTime = $array_result[0]['bestracetime'];
$timeDiff = $row['bestracetime'] - $bestTime;
$format_timeDiff = formatTime($timeDiff, true);
$time = formatTime($row['bestracetime'], true);
$points = $array_result[0]['map_points'];
$pointsmap[] = array('nick' => $row['nickname'],'totalpoints' => +$points);

		echo "<tr>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$rank."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$row['nickname']."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$time."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">+".$format_timeDiff."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$points."</td>";
		echo "</tr>";
}
echo'</table>';
echo '<br>';
//3rd Map
$link = mysqli_connect("host", "user", "password", "pyplanet", "3306");
if (!$link) {
    echo "Error: Unable to connect to MySQL." . PHP_EOL;
    echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

$MapRequest = "SELECT *
FROM `map`
WHERE `id` =1";

$result = mysqli_query($link, $MapRequest);

if (!$result) {
    $message  = "Invalid query: " . mysqli_connect_error() . "\n";
    $message .= "Whole query: " . $MapRequest;
    die($message);
}

$Mapname = '$fffMapName: &nbsp; &nbsp; &nbsp;';
while($row = mysqli_fetch_array($result)) {
	$MapColor = '$fff'.$row[4].'';
  echo "".$cp->toHTML($Mapname)."".$cp->toHTML($MapColor)."".$row[4]."";
  echo '<br>';
}

$RecordRequest = "SELECT * FROM player INNER JOIN match_results ON match_results.player_id = player.id Where match_results.map_id=1 ORDER BY match_results.rank ASC";

$result = mysqli_query($link, $RecordRequest);

if (!$result) {
    $message  = "Invalid query: " . mysqli_connect_error() . "\n";
    $message .= "Whole query: " . $RecordRequest;
    die($message);
}

	echo '<table width=\"100%\" border=\"0\" align=\"center\">
  <tr">
    <td width=\"60\" class=\"tablehead\" bgcolor="#FFFFF">Rank</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Nickname</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Time</td>
	<td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">TimeDifference</td>
    <td width=\"80\" class=\"tablehead\" bgcolor="#FFFFF">Points</td>
</td>';

$rank = 0;
$points = array();
$array_result = array();
$pointsmap = array();
while ($row = mysqli_fetch_array($result)) {
$array_result[] = $row;
$rank++;
$bestTime = $array_result[0]['bestracetime'];
$timeDiff = $row['bestracetime'] - $bestTime;
$format_timeDiff = formatTime($timeDiff, true);
$time = formatTime($row['bestracetime'], true);
$points = $array_result[0]['map_points'];
$pointsmap[] = array('nick' => $row['nickname'],'totalpoints' => +$points);

		echo "<tr>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$rank."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$row['nickname']."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$time."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">+".$format_timeDiff."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$points."</td>";
		echo "</tr>";
}
echo'</table>';
echo '<br>';
//var_dump($pointsmap);

// begin the iteration for grouping bank name and calculate the amount
$amount = array();
foreach($pointsmap as $bank) {
    $index = bank_exists($bank['nick'], $amount);
    if ($index < 0) {
        $amount[] = $bank;
    }
    else {
        $amount[$index]['totalpoints'] +=  $bank['totalpoints'];
    }
}
print_r($amount); //display 

// for search if a bank has been added into $amount, returns the key (index)
function bank_exists($bankname, $array) {
    $result = -1;
    for($i=0; $i<sizeof($array); $i++) {
        if ($array[$i]['nick'] == $bankname) {
            $result = $i;
            break;
        }
    }
    return $result;
}
echo '<br>';
$MapColor = '$fffTotal Points Gathered on all 3 Maps:';
echo $cp->toHTML($MapColor);
echo '<table width=\"100%\" border=\"0\" align=\"center\">
  <tr>
    <td width=\"60\" class=\"tablehead\" bgcolor="#FFFFF">Rank</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">Nickname</td>
    <td width=\"150\" class=\"tablehead\" bgcolor="#FFFFF">TotalPoints</td>
</tr>';

$rank = 1;
$target = 16;
array_multisort($price, SORT_DESC, $amount);
foreach ($amount as $key => $total){
	if ($key >= $target) {
		break;
	}
	krsort($total);
echo "<tr>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$rank."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$total['nick']."</td>";
		echo "<td class=\"celltext\" bgcolor=\"#FFFFF\">".$total['totalpoints']."</td>";
	echo "</tr>";
	$rank++;
}
echo '</table>';
?>
