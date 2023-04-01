import pytest
from src.core.Matcher import get_weight, get_email_info
from unittest.mock import patch

class Test_Matcher_TA_Scheduling:

    def test_get_weight(self):
        assert get_weight("preferred") == 2
        assert get_weight(True) == 2
        assert get_weight(False) == 1
        assert get_weight(None) == 1
        assert get_weight("normal") == 1

    def test_get_email_info(self):
        email = "tworpo@seattleu.edu"
        courseID = "CPSC-2430"

        # set up mock values for get_email_info_for_Matcher
        email_cGPA = 3.7
        email_GPA = 3.5
        is_email_ref = True
        email_preferenceLevel = "preferred"

        with patch('src.db.DBQuerrier.get_email_info_for_Matcher') as mock_get_email_info_for_Matcher:
            mock_get_email_info_for_Matcher.return_value = (email_cGPA, email_GPA, is_email_ref, email_preferenceLevel)

            email_cGPA_result, email_GPA_result, email_ref_weight, email_preferenceLevel_weight = get_email_info(email,
                                                                                                                 courseID)

            assert email_cGPA_result == email_cGPA
            assert email_GPA_result == email_GPA
            assert email_ref_weight == 2
            assert email_preferenceLevel_weight == 2

    def test_get_compare(self):
        pass

    def test_get_student_priority_sort(self):
        pass

    def test_assign_faculty_preferred_students_to_course(self):
        pass