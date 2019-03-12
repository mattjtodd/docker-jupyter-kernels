CREATE DATABASE telemetry;

USE telemetry;

CREATE TABLE wheel_steer (
  timestamp decimal,
  wheel varchar(2),
  action varchar(2),
  current decimal,
  status decimal,
  speed decimal,
  pid_last_output decimal,
  pid_last_delta decimal,
  pid_set_point decimal,
  pid_i decimal,
  pid_d decimal,
  pid_last_error decimal);
 
ALTER TABLE wheel_steer ADD INDEX (timestamp);

CREATE TABLE wheel_steer_interest (
  start_timestamp decimal,
  end_timestamp decimal,
  INDEX (start_timestamp),
  INDEX (end_timestamp)
);