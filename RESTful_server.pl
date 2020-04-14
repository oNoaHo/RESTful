#!/usr/bin/perl -w

use Dancer;
use Data::Dumper;
use Dancer::Request;
#set serializer => 'XML';
set serializer => 'JSON'; #un-comment this for json format responses
 
get '/' => sub{
    return {message => "First rest Web Service with Perl and Dancer"};
};

get '/users/:name' => sub {
    my $user = params->{name};
    my $params = request->params;
    return {message => Dumper($params)};
#    return {message => "Hello $user"};
};
get '/users/:name/:record' => sub {
    my $user = params->{name};
    my $record = params->{record};
    return {message => "Hello $user $record"};
};
 
get '/users' => sub{
    my %users = (
        userA => {
            id   => "1",
            name => "Carlos",
        },
        userB => {
            id   => "2",
            name => "Andres",
        },
        userC => {
            id   => "3",
            name => "Bryan",
        },
    );

    return \%users;
};

dance;