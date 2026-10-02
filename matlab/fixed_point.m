function [root, T] = fixed_point(g, x0, tol, max_iter)
% =========================================================================
% خوارزمية طريقة النقطة الثابتة (Fixed-Point Iteration)
% مادة: التحليل العددي (Numerical Analysis)
% =========================================================================
% الوظيفة:
%   إيجاد جذر المعادلة f(x) = 0 عن طريق إعادة صياغتها على شكل:
%   x = g(x)
%   ثم تطبيق التكرار المتتالي: x_{n+1} = g(x_n)
%   ويشترط للتقارب أن يكون: |g'(x)| < 1 في جوار الجذر.
%
% المدخلات (Inputs):
%   g        : دالة التكرار كـ function handle، مثال: @(x) (x + 2).^(1/3)
%   x0       : التخمين الابتدائي (افتراضياً: 1.5)
%   tol      : الدقة المطلوبة (افتراضياً: 1e-4)
%   max_iter : أقصى عدد تكرارات (افتراضياً: 50)
%
% المخرجات (Outputs):
%   root     : القيمة التقريبية للنقطة الثابتة (الجذر)
%   T        : جدول التكرارات التفصيلي
% =========================================================================

    if nargin < 1 || isempty(g), g = @(x) (x + 2).^(1/3); end
    if nargin < 2 || isempty(x0), x0 = 1.5; end
    if nargin < 3 || isempty(tol), tol = 1e-4; end
    if nargin < 4 || isempty(max_iter), max_iter = 50; end

    if ischar(g) || isstring(g), g = str2func(['@(x) ' char(g)]); end

    fprintf('\n=================================================================\n');
    fprintf('  طريقة النقطة الثابتة (Fixed-Point Iteration: x = g(x))\n');
    fprintf('=================================================================\n');
    fprintf('التخمين الابتدائي: x0 = %.4f\n', x0);
    fprintf('الدقة المطلوبة: %e\n', tol);
    fprintf('-----------------------------------------------------------------\n');

    fprintf('%-4s | %-12s | %-12s | %-12s\n', ...
        'n', 'x_n', 'g(x_n)', 'الخطأ |x_{n+1}-x_n|');
    fprintf('-----------------------------------------------------------------\n');

    table_data = [];
    x_curr = x0;

    for n = 1:max_iter
        x_next = g(x_curr);
        err = abs(x_next - x_curr);

        fprintf('%-4d | %12.6f | %12.6f | %12.6e\n', ...
            n, x_curr, x_next, err);

        table_data = [table_data; n, x_curr, x_next, err]; %#ok<AGROW>

        % فحص التباعد الانفجاري (Divergence)
        if isnan(x_next) || isinf(x_next) || err > 1e10
            error('خطأ: التكرار متباعد (Divergent)! تأكد أن شرط التقارب |g''(x)| < 1 محقق.');
        end

        if err < tol
            fprintf('-----------------------------------------------------------------\n');
            fprintf('✓ تم الوصول للنقطة الثابتة بنجاح عند التكرار n = %d\n', n);
            fprintf('✓ الجذر التقريبي: x ≈ %.6f\n', x_next);
            fprintf('✓ الخطأ المتبقي: %e\n', err);
            root = x_next;
            T = table_data;
            return;
        end

        x_curr = x_next;
    end

    root = x_curr;
    T = table_data;
    warning('تم بلوغ الحد الأقصى للتكرارات دون الوصول للدقة التامة.');
end
