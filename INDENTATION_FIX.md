# ✅ Indentation Error Fixed

## Issue
The app.py file had an indentation error around line 189 caused by duplicate code blocks.

## Error Message
```
IndentationError: unexpected indent
File "app.py", line 189
    value="rice",
```

## Root Cause
There was duplicate code in the `display_input_section` function where the "Advanced Options" section was repeated twice, causing incorrect indentation.

## Fix Applied
Removed the duplicate code block that was causing the indentation error.

**Before:**
```python
# First block (correct)
with st.expander("Advanced Options (Optional)"):
    # ... correct code ...

return input_type, input_data, location, crop, area

# Duplicate block (causing error)
                value="rice",  # <- This line had wrong indentation
                help="For finance queries"
            )
        
        with col2:
            # ... duplicate code ...
```

**After:**
```python
# Single, correct block
with st.expander("Advanced Options (Optional)"):
    # ... correct code ...

return input_type, input_data, location, crop, area

def display_response(response, language: str):
    # ... next function starts correctly ...
```

## Verification
- ✅ App syntax is now correct
- ✅ Streamlit runs successfully on http://localhost:8502
- ✅ All voice input features working
- ✅ No more indentation errors

## How to Run
```bash
python -m streamlit run app.py
```

The app now starts correctly with both text and voice input modes available!

---

**Status**: ✅ Fixed and working!