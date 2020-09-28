import pymysql
import sys
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Flask
from flask_restplus import Api, Resource, fields


@app.route('/create', methods=['POST'])
def create_student():
		try:
			_json = request.json
			_author_name = _json['author_name']
			_book_name = _json['book_name']
			_isbn = _json['isbn']
			sqlQuery = "INSERT INTO books(author_name, book_name, isbn) VALUES(%s, %s, %s)"
			data = ( _author_name, _book_name, _isbn,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, data)
			conn.commit()
			res = jsonify('Book added successfully.')
			res.status_code = 200
			return res

		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()

@app.route('/book')
def getAllBooks():
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM books")
			rows = cursor.fetchall()
			res = jsonify(rows)
			res.status_code = 200
			return res
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
			
@app.route('/books/<int:id>')
def book(id):
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM books WHERE id=%s", id)
			row = cursor.fetchone()
			res = jsonify(row)
			res.status_code = 200
			return res
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()

@app.route('/update', methods=['PUT'])
def update_book():
		try:
			_json = request.json
			_author_name = _json['author_name']
			_id = _json['id']
			_book_name = _json['book_name']
			_isbn = _json['isbn']

			sql = "UPDATE student SET author_name=%s, book_name=%s, isbn=%s WHERE id=%s"
			data = (_author_name, _book_name, _isbn, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			res = jsonify('Book entry updated')
			res.status_code = 200
			return res
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_book(id):
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("DELETE FROM books WHERE id=%s", (id,))
			conn.commit()
			res = jsonify('Book removed successfully.')
			res.status_code = 200
			return res
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
			
@app.errorhandler(404)
def not_found(error=None):
	    message = {
	        'status': 404,
	        'message': 'RESOURCE NOT FOUND' + request.url,
	    }
	    res = jsonify(message)
	    res.status_code = 404
	    return res
			
if __name__ == "__main__":
	    app.run()	