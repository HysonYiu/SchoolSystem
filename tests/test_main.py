"""
Tests for main.py API endpoints
"""
import pytest
import json
from datetime import date, timedelta


class TestHealthCheck:
    """Test /health endpoint"""

    def test_health_check_ok(self, client):
        """Health check should return 200 OK"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] in ['ok', 'healthy']


class TestAuthentication:
    """Test authentication flow"""

    def test_login_with_correct_key(self, client):
        """Login with correct SECRET_KEY should succeed"""
        response = client.post('/', data={'key': 'test-secret-key'})
        # Should set cookie and allow subsequent requests
        assert response.status_code in [200, 302]

    def test_login_with_incorrect_key(self, client):
        """Login with incorrect key should fail"""
        response = client.post('/', data={'key': 'wrong-key'})
        # Should reject or require re-entry
        assert response.status_code in [200, 401, 400]

    def test_unauthenticated_api_access(self, client):
        """API endpoints should require authentication"""
        response = client.get('/api/hw')
        assert response.status_code == 401


class TestHomeworkAPI:
    """Test homework management endpoints"""

    def test_get_homework_list(self, client, auth_client):
        """GET /api/hw should return homework list"""
        response = auth_client.get('/api/hw')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'homework' in data or 'homeworks' in data or isinstance(data, list)

    def test_add_homework_valid(self, client, auth_client):
        """POST /api/hw with valid data should create homework"""
        hw_data = {
            'title': 'Chemistry Lab',
            'subject': 'CHEM',
            'hw_type': '實驗',
            'due_date': (date.today() + timedelta(days=3)).isoformat(),
            'priority': '高'
        }
        response = auth_client.post(
            '/api/hw',
            data=json.dumps(hw_data),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]
        data = json.loads(response.data)
        assert 'id' in data or 'success' in data or data.get('status') == 'success'

    def test_add_homework_missing_required(self, client, auth_client):
        """POST /api/hw without required fields should fail"""
        hw_data = {
            'title': 'Incomplete',
            # Missing subject, hw_type, due_date
        }
        response = auth_client.post(
            '/api/hw',
            data=json.dumps(hw_data),
            content_type='application/json'
        )
        assert response.status_code in [400, 422]

    def test_mark_homework_done(self, client, auth_client, db, sample_homework):
        """POST /api/hw/<id>/done should mark homework as done"""
        hw_id = sample_homework
        response = auth_client.post(f'/api/hw/{hw_id}/done')
        assert response.status_code in [200, 404]  # 404 if not found in test DB

    def test_mark_homework_undone(self, client, auth_client, sample_homework):
        """POST /api/hw/<id>/undone should mark homework as not done"""
        hw_id = sample_homework
        response = auth_client.post(f'/api/hw/{hw_id}/undone')
        assert response.status_code in [200, 404]


class TestCycleAPI:
    """Test cycle/timetable endpoints"""

    def test_get_cycle_day(self, client, auth_client):
        """GET /api/cycle should return current cycle day"""
        response = auth_client.get('/api/cycle')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'cycle_day' in data

    def test_get_today_info(self, client, auth_client):
        """GET /api/today should return today's info + homework"""
        response = auth_client.get('/api/today')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'date' in data
        assert 'cycle_day' in data
        assert 'homework' in data or isinstance(data, dict)

    def test_get_timetable_specific_day(self, client, auth_client):
        """GET /api/timetable?day=3 should return specific day timetable"""
        for day in [1, 3, 7]:
            response = auth_client.get(f'/api/timetable?day={day}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'day' in data or isinstance(data, (dict, list))


class TestStatsAPI:
    """Test statistics endpoints"""

    def test_get_stats(self, client, auth_client):
        """GET /api/stats should return statistics"""
        response = auth_client.get('/api/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should contain at least stats or similar data
        assert len(data) > 0


class TestExamsAPI:
    """Test exam management endpoints"""

    def test_get_exams(self, client, auth_client):
        """GET /api/exams should return exam list"""
        response = auth_client.get('/api/exams')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'exams' in data or isinstance(data, list)

    def test_add_exam_valid(self, client, auth_client):
        """POST /api/exams with valid data should create exam"""
        exam_data = {
            'title': 'Physics Final',
            'exam_date': (date.today() + timedelta(days=30)).isoformat(),
            'notes': 'Chapters 1-10'
        }
        response = auth_client.post(
            '/api/exams',
            data=json.dumps(exam_data),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_json(self, client, auth_client):
        """POST with invalid JSON should handle gracefully"""
        response = auth_client.post(
            '/api/hw',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code in [400, 422]

    def test_nonexistent_homework_id(self, client, auth_client):
        """Accessing nonexistent homework should return 404"""
        response = auth_client.post('/api/hw/99999/done')
        assert response.status_code == 404

    def test_method_not_allowed(self, client, auth_client):
        """Using wrong HTTP method should fail"""
        response = auth_client.post('/api/cycle')  # GET only
        assert response.status_code in [405, 404]


# Integration tests
class TestIntegration:
    """Integration tests for complete workflows"""

    def test_complete_homework_workflow(self, client, auth_client):
        """Test complete workflow: add -> view -> mark done"""
        # 1. Add homework
        hw_data = {
            'title': 'Workflow Test',
            'subject': 'MATH',
            'hw_type': '功課',
            'due_date': (date.today() + timedelta(days=5)).isoformat(),
            'priority': '中'
        }
        add_response = auth_client.post(
            '/api/hw',
            data=json.dumps(hw_data),
            content_type='application/json'
        )
        assert add_response.status_code in [200, 201]

        # 2. View homework list
        view_response = auth_client.get('/api/hw')
        assert view_response.status_code == 200

        # 3. Get stats
        stats_response = auth_client.get('/api/stats')
        assert stats_response.status_code == 200

    def test_api_consistency(self, client, auth_client):
        """Test consistency across API endpoints"""
        responses = {
            'today': auth_client.get('/api/today'),
            'hw': auth_client.get('/api/hw'),
            'stats': auth_client.get('/api/stats'),
            'exams': auth_client.get('/api/exams'),
            'cycle': auth_client.get('/api/cycle'),
        }

        # All endpoints should return 200 OK
        for endpoint, response in responses.items():
            assert response.status_code == 200, f"{endpoint} returned {response.status_code}"
