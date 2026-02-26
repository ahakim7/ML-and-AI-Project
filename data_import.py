import pandas as pd

existing_file_types = ["flic", "g", "md"]
existing_timestamps = ['20251110', '20251127', '20260109']


def timestamp_cutter(timestamp: str) -> str:
	"""
	removes timezone specifications and hundreds of seconds
	:param timestamp: 
	:return: 
	"""
	timestamp = timestamp.split("+")[0]
	return timestamp.split(".")[0]
	

def get_combined_file(file_type: str, timestamp: str) -> pd.DataFrame:
	"""
	Combines and prepares data, returning a neat and tidy DataFrame.
	:param file_type: either 'flic', 'g', or 'md' (these are accessible as strings in the data_import.existing_file_types global variable)
	:param timestamp: yyyymmdd format (we have 20251110, 20251127, and 20260109 | these are accessible as strings in the data_import.existing_timestamps global variable)
	:return: pandas dataframe
	"""
	match file_type:
		case 'flic':
			df = pd.read_csv(f"./data/flic_button_data_export_{timestamp}.csv")
			df = df.drop(['ruuvi', 'aplicom', 'companyid'])
		case 'g':
			df = pd.read_csv(f"./data/g_data_export_{timestamp}.csv")
		case 'md':
			df = pd.read_csv(f"./data/md30_export_{timestamp}.csv")
			df = df.drop(['aplicom', 'hexdata', 'crc'])
		case _:
			raise ValueError("Invalid file format")
	
	# conver to timestamp (without timezones and hundreds of seconds)
	df["ts"] = df["ts"].apply(timestamp_cutter)
	df["ts"] = pd.to_datetime(df["ts"], format = "%Y-%m-%d %H:%M:%S")
	
	# drop empty columns
	df = df.dropna(axis = 1, how = "all")
	
	# placeholder for later clearing
	match file_type:
		case 'flic':
			pass
		case 'g':
			pass
		case 'md':
			pass
	
	return df


if __name__ == '__main__':
	for f_type in existing_file_types:
		df_out = get_combined_file(f_type, '20251110')
		#print(df_out.columns)
