% Customer Support Expert System knowledge base
% Expanded and improved by Samuel Kofi Ntem Amankwah


% KNOWN SUPPORT ISSUES

issue(login_issue).
issue(order_delayed).
issue(order_missing).
issue(billing_error).
issue(defective_product).
issue(no_internet_connection).
issue(slow_internet).
issue(subscription_cancellation).

% New issues
issue(password_reset).
issue(account_locked).
issue(app_crash).
issue(network_error).
issue(refund_request).
issue(wrong_item_received).
issue(duplicate_charge).


% KEYWORDS (CLASSIFICATION)


% Login
keyword(login_issue, login).
keyword(login_issue, password).
keyword(login_issue, signin).
keyword(login_issue, account).

% Orders
keyword(order_delayed, delayed).
keyword(order_delayed, late).
keyword(order_delayed, tracking).
keyword(order_delayed, shipment).

keyword(order_missing, missing).
keyword(order_missing, not_delivered).
keyword(order_missing, not_received).

% Billing
keyword(billing_error, billing).
keyword(billing_error, charged).
keyword(billing_error, invoice).
keyword(billing_error, payment).

% Product issues
keyword(defective_product, broken).
keyword(defective_product, damaged).
keyword(defective_product, defective).
keyword(defective_product, faulty).

% Internet
keyword(no_internet_connection, no_connection).
keyword(no_internet_connection, disconnected).
keyword(no_internet_connection, offline).

keyword(slow_internet, slow).
keyword(slow_internet, buffering).
keyword(slow_internet, lag).

% Subscription
keyword(subscription_cancellation, cancel).
keyword(subscription_cancellation, unsubscribe).
keyword(subscription_cancellation, subscription).


% NEW KEYWORDS


% Password reset
keyword(password_reset, reset).
keyword(password_reset, forgot).
keyword(password_reset, recover).

% Account locked
keyword(account_locked, locked).
keyword(account_locked, blocked).
keyword(account_locked, suspended).

% App crash
keyword(app_crash, crash).
keyword(app_crash, freeze).
keyword(app_crash, stop).
keyword(app_crash, closing).

% Network error
keyword(network_error, error).
keyword(network_error, timeout).
keyword(network_error, failed).

% Refund
keyword(refund_request, refund).
keyword(refund_request, return).
keyword(refund_request, money_back).

% Wrong item
keyword(wrong_item_received, wrong_item).
keyword(wrong_item_received, incorrect).
keyword(wrong_item_received, mismatch).

% Duplicate charge
keyword(duplicate_charge, duplicate).
keyword(duplicate_charge, double_charge).
keyword(duplicate_charge, twice).


% SOLUTIONS


solution(login_issue, 'Reset your password from the Forgot Password page, then try logging in again.').
solution(order_delayed, 'Your order is in transit. Please use your tracking link and allow 24 hours for status updates.').
solution(order_missing, 'We are sorry about this. Please confirm your shipping address and contact support with your order ID for an urgent trace.').
solution(billing_error, 'Please review your invoice and share the billing reference number so we can investigate and reverse any incorrect charge.').
solution(defective_product, 'Please upload photos of the product and packaging. We will arrange a replacement or refund.').
solution(no_internet_connection, 'Restart your router, check cable connections, and confirm service status in your area.').
solution(slow_internet, 'Restart your router, reduce connected devices, and run a speed test. If the issue persists, we will escalate to network support.').
solution(subscription_cancellation, 'Open Account Settings > Subscription > Cancel Plan, then confirm cancellation from the email we send.').

% New solutions
solution(password_reset, 'Use the Forgot Password option and follow the instructions sent to your email.').
solution(account_locked, 'Your account may be temporarily locked. Wait a few minutes or contact support to unlock it.').
solution(app_crash, 'Restart the app or reinstall it. Ensure you are using the latest version.').
solution(network_error, 'Check your internet connection and try again. If the issue persists, try later.').
solution(refund_request, 'Please provide your order ID and reason for refund. We will process it within 3-5 business days.').
solution(wrong_item_received, 'We apologize. Please send a photo and your order ID so we can arrange a replacement.').
solution(duplicate_charge, 'Please share your transaction details so we can verify and refund the extra charge.').


% ESCALATION

escalation_message('I could not confidently diagnose this issue. Please escalate to a human support agent with customer details and screenshots.').


% IMPROVED DIAGNOSIS LOGIC


% Case-insensitive keyword matching
matches(Text, Keyword) :-
    downcase_atom(Text, LowerText),
    downcase_atom(Keyword, LowerKeyword),
    sub_atom(LowerText, _, _, _, LowerKeyword).

% Find best matching issue based on keyword frequency
diagnose(Text, Issue) :-
    findall(I,
        (issue(I),
         keyword(I, Keyword),
         matches(Text, Keyword)),
    Issues),
    Issues \= [],
    most_frequent(Issues, Issue),
    !.

diagnose(_, unknown_issue).


% HELPER RULES


most_frequent(List, Most) :-
    sort(List, Unique),
    count_all(Unique, List, Counts),
    max_member(_-Most, Counts).

count_all([], _, []).
count_all([H|T], List, [Count-H|Rest]) :-
    count(H, List, Count),
    count_all(T, List, Rest).

count(_, [], 0).
count(X, [X|T], N) :-
    count(X, T, N1),
    N is N1 + 1.
count(X, [_|T], N) :-
    count(X, T, N).

% RESOLUTION


resolve_issue(Issue, Message) :-
    solution(Issue, Message),
    !.

resolve_issue(unknown_issue, Message) :-
    escalation_message(Message).


% MAIN ENTRY POINT


recommendation(Text, Message) :-
    diagnose(Text, Issue),
    resolve_issue(Issue, Message).


% UTILITY


list_issue(Issue) :- solution(Issue, _).