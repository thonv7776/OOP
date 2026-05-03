import pytest
from library_item import LibraryItem


class TestLibraryItemInitialization:
    """Test suite for LibraryItem initialization"""
    
    def test_init_with_all_parameters(self):
        """Test LibraryItem initialization with name, artist, and rating"""
        item = LibraryItem("Test Song", "Test Artist", 5)
        assert item.name == "Test Song"
        assert item.artist == "Test Artist"
        assert item.rating == 5
        assert item.play_count == 0

    def test_init_with_default_rating(self):
        """Test LibraryItem initialization with default rating of 0"""
        item = LibraryItem("Test Song", "Test Artist")
        assert item.name == "Test Song"
        assert item.artist == "Test Artist"
        assert item.rating == 0
        assert item.play_count == 0

    def test_init_with_empty_strings(self):
        """Test LibraryItem initialization with empty strings"""
        item = LibraryItem("", "", 3)
        assert item.name == ""
        assert item.artist == ""
        assert item.rating == 3
        assert item.play_count == 0


class TestLibraryItemPlayCount:
    """Test suite for play_count functionality"""
    
    def test_play_count_initialized_to_zero(self):
        """Test that play_count is initialized to 0"""
        item = LibraryItem("Song", "Artist", 3)
        assert item.play_count == 0

    def test_play_count_can_be_incremented(self):
        """Test that play_count can be incremented"""
        item = LibraryItem("Song", "Artist", 3)
        item.play_count += 1
        assert item.play_count == 1

    def test_play_count_multiple_increments(self):
        """Test that play_count can be incremented multiple times"""
        item = LibraryItem("Song", "Artist", 3)
        for i in range(5):
            item.play_count += 1
        assert item.play_count == 5


class TestLibraryItemRating:
    """Test suite for rating functionality"""
    
    def test_rating_can_be_set(self):
        """Test that rating can be set"""
        item = LibraryItem("Song", "Artist", 2)
        assert item.rating == 2

    def test_rating_can_be_changed(self):
        """Test that rating can be changed after initialization"""
        item = LibraryItem("Song", "Artist", 2)
        item.rating = 5
        assert item.rating == 5

    def test_rating_with_zero_value(self):
        """Test rating with zero value"""
        item = LibraryItem("Song", "Artist", 0)
        assert item.rating == 0

    def test_rating_with_max_value(self):
        """Test rating with maximum value"""
        item = LibraryItem("Song", "Artist", 5)
        assert item.rating == 5

    def test_rating_with_negative_value(self):
        """Test rating can be set to negative (no validation in LibraryItem)"""
        item = LibraryItem("Song", "Artist", -1)
        assert item.rating == -1


class TestLibraryItemStarsMethod:
    """Test suite for stars() method"""
    
    def test_stars_with_zero_rating(self):
        """Test stars() returns empty string for rating 0"""
        item = LibraryItem("Song", "Artist", 0)
        assert item.stars() == ""

    def test_stars_with_one_rating(self):
        """Test stars() returns one star for rating 1"""
        item = LibraryItem("Song", "Artist", 1)
        assert item.stars() == "*"

    def test_stars_with_five_rating(self):
        """Test stars() returns five stars for rating 5"""
        item = LibraryItem("Song", "Artist", 5)
        assert item.stars() == "*****"

    def test_stars_with_three_rating(self):
        """Test stars() returns three stars for rating 3"""
        item = LibraryItem("Song", "Artist", 3)
        assert item.stars() == "***"

    def test_stars_with_modified_rating(self):
        """Test stars() reflects changes to rating"""
        item = LibraryItem("Song", "Artist", 2)
        assert item.stars() == "**"
        item.rating = 4
        assert item.stars() == "****"

    def test_stars_with_negative_rating(self):
        """Test stars() with negative rating returns empty string"""
        item = LibraryItem("Song", "Artist", -1)
        assert item.stars() == ""


class TestLibraryItemInfoMethod:
    """Test suite for info() method"""
    
    def test_info_format(self):
        """Test info() returns correctly formatted string"""
        item = LibraryItem("What a Wonderful World", "Louis Armstrong", 5)
        result = item.info()
        assert "What a Wonderful World" in result
        assert "Louis Armstrong" in result
        assert "*****" in result

    def test_info_with_zero_rating(self):
        """Test info() with zero rating"""
        item = LibraryItem("Song", "Artist", 0)
        result = item.info()
        assert result == "Song - Artist "

    def test_info_with_three_rating(self):
        """Test info() with three rating"""
        item = LibraryItem("Count on Me", "Bruno Mars", 3)
        result = item.info()
        assert result == "Count on Me - Bruno Mars ***"

    def test_info_with_modified_rating(self):
        """Test info() reflects rating changes"""
        item = LibraryItem("Song", "Artist", 1)
        assert item.info() == "Song - Artist *"
        item.rating = 4
        assert item.info() == "Song - Artist ****"

    def test_info_with_special_characters(self):
        """Test info() with special characters in name and artist"""
        item = LibraryItem("Song's Name (Remix)", "Artist & Co.", 4)
        result = item.info()
        assert "Song's Name (Remix)" in result
        assert "Artist & Co." in result


class TestLibraryItemEdgeCases:
    """Test suite for edge cases"""
    
    def test_long_song_name(self):
        """Test with very long song name"""
        long_name = "A" * 100
        item = LibraryItem(long_name, "Artist", 3)
        assert item.name == long_name
        assert long_name in item.info()

    def test_unicode_characters(self):
        """Test with unicode characters"""
        item = LibraryItem("你好世界", "アーティスト", 3)
        assert item.name == "你好世界"
        assert item.artist == "アーティスト"
        assert "你好世界" in item.info()

    def test_special_characters(self):
        """Test with special characters"""
        item = LibraryItem("!@#$%^&*()", "~`<>?", 2)
        assert item.name == "!@#$%^&*()"
        assert item.artist == "~`<>?"
        assert "!@#$%^&*()" in item.info()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
