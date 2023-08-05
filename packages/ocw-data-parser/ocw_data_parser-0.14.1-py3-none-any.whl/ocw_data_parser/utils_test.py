import os
import json
import pytest
from tempfile import TemporaryDirectory
import ocw_data_parser.test_constants as constants
from ocw_data_parser.utils import update_file_location, get_binary_data, get_correct_path, load_json_file, print_error, print_success, \
    htmlify, parse_all


def test_update_local_file_location(ocw_parser):
    """
    Extract local course media, update the location of one of the files 
    and then assert that the location has indeed changed
    """
    ocw_parser.extract_media_locally()
    assert len(ocw_parser.master_json["course_files"]) > 0, "test course has no local media to test"
    test_file = ocw_parser.master_json["course_files"][0]
    original_location = test_file["file_location"]
    update_file_location(ocw_parser.master_json,
                            "test_location", obj_uid=test_file["uid"])
    assert original_location != ocw_parser.master_json["course_files"][0]["file_location"], "failed to update local file location"

def test_update_foreign_file_location(ocw_parser):
    """
    Extract foreign course media, update the location of one of the files 
    and then assert that the location has indeed changed
    """
    ocw_parser.extract_foreign_media_locally()
    assert len(ocw_parser.master_json["course_foreign_files"]) > 0, "test course has no foreign media to test"
    test_file = ocw_parser.master_json["course_foreign_files"][0]
    original_location = test_file["file_location"]
    original_filename = test_file["link"].split("/")[-1]
    update_file_location(ocw_parser.master_json,
                            os.path.join("test_location/", original_filename))
    assert original_location != ocw_parser.master_json["course_foreign_files"][0]["file_location"], "failed to update foreign file location"

def test_get_binary_data_none(ocw_parser):
    """
    Find the first file without a datafield property and attempt to get the binary data from it
    """
    assert len(ocw_parser.master_json["course_files"]) > 0, "test course has no local media to test"
    found = False
    for media in ocw_parser.master_json["course_files"]:
        if "_datafield_image" not in media and "_datafield_file" not in media:
            found = True
            data = get_binary_data(media)
            assert data is None, "unexpected binary data in non _datafield_image or _datafield_file media"
    assert found, "test course has no file without a datafield property"

def test_get_correct_path_none(ocw_parser):
    """
    Test passing in invalid data to get_correct_path
    """
    assert get_correct_path(None) == ""

def test_load_invalid_json_file(ocw_parser):
    """
    Test passing in an invalid JSON file (this one)
    """
    with pytest.raises(json.decoder.JSONDecodeError):
        load_json_file("ocw_data_parser/ocw_data_parser_test.py")

def test_print_error(ocw_parser):
    """
    Test printing an error doesn't throw an exception
    """
    print_error("Error!")

def test_print_success(ocw_parser):
    """
    Test that printing a success message doesn't throw an exception
    """
    print_success("Success!")

def test_htmlify(ocw_parser):
    """
    Test that calling htmlify on a page returns some html and a filename
    """
    master_json = ocw_parser.get_master_json()
    course_pages = master_json.get("course_pages")
    test_page = course_pages[0]
    filename, html = htmlify(test_page)
    assert filename == test_page["uid"] + "_" + test_page["short_url"] + ".html"
    assert "<html>" in html
    assert "</html>" in html
    assert "<body>" in html
    assert "</body>" in html
    assert test_page["text"] in html

def test_parse_all():
    with TemporaryDirectory() as destination_dir:
        parse_all(constants.COURSE_DIR, destination_dir)
        assert os.path.isdir(os.path.join(destination_dir, "course-1"))
        assert os.path.isdir(os.path.join(destination_dir, "course-2"))
