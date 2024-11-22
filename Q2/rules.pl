:- use_module(library(csv)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/http_json)).

load_csv_data(File) :-
    csv_read_file(File, Rows, [functor(student), arity(4)]),
    maplist(assert, Rows).

eligible_for_scholarship(Student_ID) :-
    student(Student_ID, _, Attendance_percentage, CGPA),
    Attendance_percentage >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, _, Attendance_percentage, _),
    Attendance_percentage >= 75.

start_server(Port) :-
    http_server(http_dispatch, [port(Port)]).

:- http_handler('/', root_handler, []).
:- http_handler('/scholarship', check_scholarship, []).
:- http_handler('/exam', check_exam_permission, []).

root_handler(_Request) :-
    format('Content-type: text/plain~n~n'),
    format('Welcome to the Student Eligibility Checker API.~n'),
    format('Available endpoints:~n'),
    format('1. /scholarship?student_id=<ID> - Check scholarship eligibility~n'),
    format('2. /exam?student_id=<ID> - Check exam permission~n').

check_scholarship(Request) :-
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    (eligible_for_scholarship(Student_ID) ->
        Reply = json{student_id: Student_ID, eligible: true};
        Reply = json{student_id: Student_ID, eligible: false}),
    reply_json(Reply).

check_exam_permission(Request) :-
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    (permitted_for_exam(Student_ID) ->
        Reply = json{student_id: Student_ID, permitted: true};
        Reply = json{student_id: Student_ID, permitted: false}),
    reply_json(Reply).

:- initialization(load_csv_data('data.csv')).
:- initialization(start_server(8082)).



