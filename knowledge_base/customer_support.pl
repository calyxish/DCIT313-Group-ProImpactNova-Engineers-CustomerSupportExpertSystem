% Customer Support Expert System knowledge base
% Facts and rules for mapping customer problems to solutions.

% Known support issues
issue(login_issue).
issue(order_delayed).
issue(order_missing).
issue(billing_error).
issue(defective_product).
issue(no_internet_connection).
issue(slow_internet).
issue(subscription_cancellation).

% Keywords that help classify a free-text customer report
keyword(login_issue, login).
keyword(login_issue, password).
keyword(login_issue, signin).
keyword(login_issue, account).

keyword(order_delayed, delayed).
keyword(order_delayed, late).
keyword(order_delayed, tracking).
keyword(order_delayed, shipment).

keyword(order_missing, missing).
keyword(order_missing, not_delivered).
keyword(order_missing, not_received).

keyword(billing_error, billing).
keyword(billing_error, charged).
keyword(billing_error, invoice).
keyword(billing_error, payment).

keyword(defective_product, broken).
keyword(defective_product, damaged).
keyword(defective_product, defective).
keyword(defective_product, faulty).

keyword(no_internet_connection, no_connection).
keyword(no_internet_connection, disconnected).
keyword(no_internet_connection, offline).

keyword(slow_internet, slow).
keyword(slow_internet, buffering).
keyword(slow_internet, lag).

keyword(subscription_cancellation, cancel).
keyword(subscription_cancellation, unsubscribe).
keyword(subscription_cancellation, subscription).

% Recommended responses
solution(login_issue, 'Reset your password from the Forgot Password page, then try logging in again.').
solution(order_delayed, 'Your order is in transit. Please use your tracking link and allow 24 hours for status updates.').
solution(order_missing, 'We are sorry about this. Please confirm your shipping address and contact support with your order ID for an urgent trace.').
solution(billing_error, 'Please review your invoice and share the billing reference number so we can investigate and reverse any incorrect charge.').
solution(defective_product, 'Please upload photos of the product and packaging. We will arrange a replacement or refund.').
solution(no_internet_connection, 'Restart your router, check cable connections, and confirm service status in your area.').
solution(slow_internet, 'Restart your router, reduce connected devices, and run a speed test. If the issue persists, we will escalate to network support.').
solution(subscription_cancellation, 'Open Account Settings > Subscription > Cancel Plan, then confirm cancellation from the email we send.').

escalation_message('I could not confidently diagnose this issue. Please escalate to a human support agent with customer details and screenshots.').

% Rule: diagnose an issue from free-text input using keyword matching.
diagnose(Text, Issue) :-
    issue(Issue),
    keyword(Issue, Keyword),
    sub_atom(Text, _, _, _, Keyword),
    !.

diagnose(_, unknown_issue).

% Rule: resolve a known issue atom to a solution.
resolve_issue(Issue, Message) :-
    solution(Issue, Message),
    !.

resolve_issue(unknown_issue, Message) :-
    escalation_message(Message).

% Rule: infer a recommendation directly from free-text.
recommendation(Text, Message) :-
    diagnose(Text, Issue),
    resolve_issue(Issue, Message).

% Utility rule used by the Python UI to build menu options.
list_issue(Issue) :- solution(Issue, _).
