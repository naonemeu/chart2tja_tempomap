import re
import math
import os
import sys

# Do not modify this function during a prompt. It's final
def parse_chart_info(file_path):
    """
    Function to parse song information from a .chart file.

    Parameters:
    - file_path (str): Path to the .chart file.

    Returns:
    - res (int or None): Resolution of the chart.
    - song_info (list): List containing song information [Name, Artist].
    """
    # Open the file for reading
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # Initialize variables
        in_data_point = False
        res = None
        song_info = []
        
        # Read file line by line
        for line in file:
            # Check if the line marks the start of a data point
            if "[Song]" in line:
                in_data_point = True
                continue
            
            # Check if the line marks the end of a data point
            if "}" in line and in_data_point:
                in_data_point = False
                break
            
            # If inside a data point, parse the Resolution, Name, and Artist
            if in_data_point:
                match_resolution = re.search(r'Resolution\s*=\s*(\d+)', line)
                match_name = re.search(r'Name\s*=\s*"([^"]+)"', line)
                match_artist = re.search(r'Artist\s*=\s*"([^"]+)"', line)
                
                if match_resolution:
                    res = int(match_resolution.group(1))
                
                if match_name:
                    song_info.append(match_name.group(1))
                
                if match_artist:
                    song_info.append(match_artist.group(1))
        
        return res, song_info



# Do not modify this function during a prompt. It's final
def parse_sync_track(file_path):
    """
    Function to parse sync track information from a .chart file.

    Parameters:
    - file_path (str): Path to the .chart file.

    Returns:
    - sync_track_info (list): List containing sync track information.
    - ts_track_info (list): List containing TS track information.
    """
    # Open the file for reading
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # Initialize variables
        in_sync_track = False
        sync_track_info = []
        ts_track_info = []
        first_line_skipped = False
        
        # Read file line by line
        for line in file:
            # Check if the line marks the start of a sync track data point
            if "[SyncTrack]" in line:
                in_sync_track = True
                first_line_skipped = False
                continue
            
            # Skip the first line after entering the sync track data point
            if in_sync_track and not first_line_skipped:
                first_line_skipped = True
                continue
            
            # Check if the line marks the end of a sync track data point
            if "}" in line and in_sync_track:
                in_sync_track = False
                break
            
            # Check for TS lines
            if in_sync_track and "TS" in line:
                match_ts_info = re.search(r'(\d+)\s*=\s*TS\s*(\d+)\s*(\d+)?', line)
                if match_ts_info:
                    position = int(match_ts_info.group(1))
                    ts_up = int(match_ts_info.group(2))
                    ts_down = 2 ** int(match_ts_info.group(3)) if match_ts_info.group(3) else 4
                    ts_track_info.append([position, ts_up, ts_down])
                continue
            
            # If inside a sync track data point, parse the sync track info
            if in_sync_track:
                match_sync_info = re.search(r'(\d+)\s*=\s*B\s*(\d+)', line)
                if match_sync_info:
                    position = int(match_sync_info.group(1))
                    bpm = float(match_sync_info.group(2)) / 1000.0
                    sync_track_info.append([position, bpm])
                else:
                    sync_track_info.append([line.strip()])
        
        return sync_track_info, ts_track_info
        
        
        

def write_to_tja(file_path, song_info, sync_track_info, ts_track_info):
    """
    Function to write parsed content to a .tja file in TJA format.

    Parameters:
    - file_path (str): Path to the output .tja file.
    - song_info (list): List containing song information [Name, Artist, Resolution].
    - sync_track_info (list): List containing sync track information.
    - step (int): Number of steps for the sync track. Default is 4.
    """
    # Extracting information for .tja file
    title = song_info[0] if song_info else "Unknown Title"
    subtitle = song_info[1] if len(song_info) > 1 else ""
    bpm = sync_track_info[0][1] if sync_track_info else 120.000
    resolution = song_info[2] if len(song_info) > 2 else 192

    # Writing .tja content to the output file
    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f'TITLE: {title}\nSUBTITLE: {subtitle}\nBPM: {bpm}\nWAVE: song.ogg\nOFFSET: \nDEMOSTART: \nPREIMAGE: \nMAKER: \n\nCOURSE:Oni\nLEVEL:\nBALLOON:\nSCOREINIT:\nSCOREDIFF:\nNOTESDESIGNER3:\n\n#START\n')

        # Write sync track content
        lines_written = 0
        for i in range(1, int(sync_track_info[-1][0] / (resolution*4) + 5)):
        
            print(f"Looping for measure {i}")
            output_file.write('\n')  # Add newline after loop declaration
            
            # Write sections info
            for position, section_string in sections_info:
                if position == lines_written * resolution * 4:
                    output_file.write(f'// section {section_string}\n')
                      
            #TS/MEASURE ADJUSTEMENT HANDLER INCOMPLETE
            # # Check if a TS event matches the current position
            # for ts_position, ts_up, ts_down in ts_track_info:
                # if ts_position == lines_written * resolution * (16 * ts_up / ts_down):
                # # Calculate the step based on the TS event
                    # step = int(16 * ts_up / ts_down)
                    # # Write the TS event to the output file
                    # output_file.write(f'\n#MEASURE {ts_up}/{ts_down}\n')
                    # break
                    
            #TS/MEASURE ADJUSTEMENT HANDLER INCOMPLETE
            step = 16
   
            for j in range(step):
                bpm_change_flag = False
                position = j * resolution * (4/step) + lines_written * resolution * step
                # print(f"Checking BPM change for position {position}")
                for bpm_position, bpm_value in sync_track_info:
                    if bpm_position == position:
                        output_file.write(f'\n#BPMCHANGE {bpm_value}\n0')
                        print(f"BPM change found: {bpm_value}")
                        bpm_change_flag = True
                        break
                if not bpm_change_flag:
                    output_file.write("0")
                    # print("No BPM change found, writing 0")
            lines_written += 1
            output_file.write(",")
            # print("Adding comma to separate measures")
        # Write footer
        output_file.write('\n#END\n')




def parse_sections(file_path):
    """
    Function to parse section information from a .chart file.

    Parameters:
    - file_path (str): Path to the .chart file.

    Returns:
    - sections_info (list): List containing section information.
    """
    # Initialize section information list
    sections_info = []

    # Read the .chart file
    with open(file_path, 'r', encoding='utf-8-sig') as chart_file:
        sections_flag = False
        for line in chart_file:
            line = line.strip()  # Remove leading and trailing whitespace
            if line == '[Events]':
                sections_flag = True
                continue
            elif line == '[':
                break
            
            if sections_flag:
                match = re.search(r'^\s*(\d+)\s*=\s*E\s*"(.*?)"\s*$', line)
                if match:
                    position = int(match.group(1))
                    section_text = match.group(2)
                    if 'section' in section_text.lower():
                        sections_info.append([position, section_text.split(' ', 1)[-1].strip()])

    return sections_info

if __name__ == "__main__":
    # Check if the file path argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    # Get the file path from command-line argument
    file_path = sys.argv[1]

    # Example usage for parse_chart_info:
    resolution, song_info = parse_chart_info(file_path)
    sections_info = parse_sections(file_path)
    sync_track_info, ts_track_info = parse_sync_track(file_path)

    # Writing the parsed content to a .tja file
    output_file_path = os.path.join(os.path.dirname(file_path), "outputfile.tja")
    write_to_tja(output_file_path, song_info, sync_track_info, ts_track_info)

    if resolution is not None:
        print("Resolution found:", resolution)
        print("Song info:", song_info)
    else:
        print("Resolution not found.")
    
    if sync_track_info:
        print("Sync track info:", sync_track_info)
    else:
        print("Sync track info not found.")

    print('sections_info:')
    print(sections_info)
    
    print('ts_track_info:')
    print(ts_track_info)
